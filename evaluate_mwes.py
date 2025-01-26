from conllu import parse_incr

# helper function to retreive mwe prediction info from given token field
def get_mwe_info(token, field):
    info = ""
    
    if field == "xpos" and token[field] != None:
        temp = token["xpos"].lower()
        if temp in ["vid", "lvc", "lvcfull", "lvccause", "vpc", "vpcfull", "mvc", "iav", "irv"]:
            info = temp
    elif field == "deprel" and ":" in token[field]:
        temp = token["deprel"].split(":")[-1]
        if temp in ["vid", "lvc", "lvcfull", "lvccause", "vpc", "vpcfull", "mvc", "iav", "irv"]:
            info = temp
    
    return info    

# evaluates mwe prediction metrics for given .conllu file
def evaluate_mwes(file, field):
    token_TP = token_FP = token_FN = 0
    unit_TP  = unit_FN  = 0

    # store mwe type info
    mwe_type = [''] * 8
    
    for sentence in parse_incr(file):

        # store Per-MWE FN info
        per_mwe_fn = [False] * 8

        # first pass: get mwe types
        for token in sentence:
            
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
                            mwe_type[i] = parts[1].lower().replace('.', '')
                            per_mwe_fn[i] = True
                    continue

        # second pass: check predictions
        for token in sentence:
            misc = token["misc"]

            # case one: FP (info in XPOS / deprel but not in 10th collumn)
            if misc == None or "mwe" not in misc:
                if get_mwe_info(token, field) != "":
                    token_FP += 1
            elif misc != None and "mwe" in misc and misc["mwe"][0].isdigit():
                index = int(misc["mwe"][0])
                correct_type = mwe_type[index]

                # case two: TP (info in XPOS / deprel matches 10th collumn)
                if get_mwe_info(token, field) == correct_type:
                    token_TP += 1
                # case three: FN (info in XPOS / deprel missing but present in 10th collumn OR there is a mismatch)
                # update per_mwe FN count if needed as well
                else:
                    token_FN += 1
                    if per_mwe_fn[index] == True:
                        per_mwe_fn[index] = False
                        unit_FN += 1

        for i in range(8):
            if per_mwe_fn[i] == True:
                unit_TP += 1

    per_token_recall    = token_TP / (token_TP + token_FN)
    per_token_precision = token_TP / (token_TP + token_FP)
    per_unit_recall     = unit_TP  / (unit_TP  + unit_FN)

    print(f"Per-token recall: {round(per_token_recall, 3)}\nPer-token precision: {round(per_token_precision, 3)}\nPer-unit recall: {round(per_unit_recall, 3)}")
