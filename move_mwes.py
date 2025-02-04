from conllu import parse_incr

def move_mwes(input_file, output_file, field_in, field_out, keep=False):

    # case one: move mwe annotations from "deprel" field to "xpos"
    if field_in == "deprel" and field_out == "xpos":
        for sentence in parse_incr(input_file):
            for token in sentence:
                temp = token["deprel"].split(":")[-1]
                if temp in ["vid", "lvc", "lvcfull", "lvccause", "vpc", "vpcfull", "mvc", "iav", "irv"]:
                    token["xpos"] = temp.upper()
                    # delete mwe info from "deprel" unless otherwise specified
                    if keep == False:
                        token["deprel"] = token["deprel"].rsplit(":", 1)[0]
                else:
                    token["xpos"] = "_"

            # append modified conllu sentence to desired output file
            with open(output_file, "a") as f:
                serialized = sentence.serialize()
                f.write(serialized)
                
    # case two: move mwe annotations from "xpos" field to "deprel"
    elif field_in == "xpos" and field_out == "deprel":
        for sentence in parse_incr(input_file):
            for token in sentence:
                if token["xpos"] != None:
                    temp = token["xpos"].lower()
                    if temp in ["vid", "lvc", "lvcfull", "lvccause", "vpc", "vpcfull", "mvc", "iav", "irv"]:
                        token["deprel"] = token["deprel"] + ":" + temp
                        # delete mwe info from "xpos" unless otherwise specified
                        if keep == False:
                            token["xpos"] = "_"
                            
            # append modified conllu sentence to desired output file
            with open(output_file, "a") as f:
                serialized = sentence.serialize()
                f.write(serialized)

    # case three: move mwe annotations from "misc" field
    elif field_in == "misc":
        # store mwe type info
        mwe_type = [''] * 8
        
        for sentence in parse_incr(input_file):
            
            # first pass: get mwe types
            for token in sentence:
                if field_out == "xpos":
                    token["xpos"] = "_"
                
                misc = token["misc"]
                
                # check if misc contains mwe information
                if misc != None and "mwe" in misc:
    
                    # check if it contains mwe category information
                    if misc["mwe"] != None and len(misc["mwe"]) > 1 and misc["mwe"][1] != ';':
    
                        # store mwe type in appropriate slot
                        if misc["mwe"][0].isdigit():
                            i = int(misc["mwe"][0])
                            misc["mwe"] = misc["mwe"].replace(' ', '')
                            parts = misc["mwe"].split(':')
                            if len(parts) > 1:
                                mwe_type[i] = ":" + parts[1].lower().replace('.', '')
                        else:
                            print(sentence.metadata["sent_id"])
                        continue
    
            # second pass: edit all fields (deprel or XPOS)
            if field_out == "deprel":
                for token in sentence:
                    
                    misc = token["misc"]
                    # if token is marked as mwe, edit its deprel tag appropriately
                    if misc != None and "mwe" in misc and misc["mwe"] != None:
                        
                        i = int(misc["mwe"][0])
                        token["deprel"] = token["deprel"] + mwe_type[i]
            elif field_out == "xpos":
                for token in sentence:
                    
                    misc = token["misc"]
                    # if token is marked as mwe, edit its XPOS tag appropriately
                    if misc != None and "mwe" in misc and misc["mwe"] != None:
                        
                        i = int(misc["mwe"][0])
                        token["xpos"] = mwe_type[i].upper()[1:]
            else:
                print("Error: Unexpected field input")
        
            # append altered conllu sentence to desired output file
            with open(output_file, "a") as f:
                serialized = sentence.serialize()
                f.write(serialized)
    else:
        print("Error: Unexpected field input")
