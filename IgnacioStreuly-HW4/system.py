import operator


def main():
    count_table = {}
    likelihood_table = {}

    total_words = 0
    total_pos_tags = 0


    with open("training_corpus.pos") as f:

        for line in f:
            array = line.split("\t")
            if len(array) < 2:
                continue

            value = array[0]
            pos = array[1]
            pos = pos.replace("\n", "")

            if not pos in count_table:
                count_table[pos]= 1
                total_pos_tags += 1

            if pos in count_table:
                count_table[pos] += 1
            total_words += 1

        # likelihood_table population
        for key, value in count_table.iteritems():
            likelihood_table[key] = float(count_table[key])/total_words

    count_table_words = {}
    likelihood_table_words = {}

    with open("training_corpus.pos") as infile:
        for line in infile:
            seq = line.split("\t")
            if len(seq) < 2:
                continue

            value = seq[0]
            pos = seq[1]
            pos = pos.replace("\n", "")

            if not value in count_table_words:
                count_table_words[value] = {}
                count_table_words[value][pos]=1

            if value in count_table_words:
                if not pos in count_table_words[value]:
                    count_table_words[value][pos]=1
                else:
                    count_table_words[value][pos]+=1

        # likelihood_table_words population
        for key, value in count_table_words.iteritems():
            if len(value) == 1:
                likelihood_table_words[key] = {}
                likelihood_table_words[key][value.keys()[0]]=1.0

            elif len(value) > 1:
                word = key
                likelihood_table_words[word] = {}

                pos_sums = 0
                for key, val in value.iteritems():
                    pos_sums += val

                for key, val in value.iteritems():
                    likelihood_table_words[word][key] = float(val)/pos_sums


    bigram_table = {}
    bigram_likelihood_table = {}

    file = open("training_corpus.pos", "r").read()

    lines = file.splitlines()
    total_lines_bigrams = 0

    for i in range(len(lines)):

        line = lines[i].split("\t")

        try:
            next_line = lines[i+1].split("\t")
        except:
            continue

        if len(line) < 2 or len(next_line) <2:
            continue

        line = line[1]
        next_line = next_line[1]
        combination = line, next_line

        if not combination in bigram_table:
            bigram_table[combination] = 1

        if combination in bigram_table:
            bigram_table[combination] += 1

        total_lines_bigrams+=1



    # populate bigram_likelihood_table
    for key, value in bigram_table.iteritems():
        bigram_likelihood_table[key] = float(bigram_table[key])/total_lines_bigrams


    # populate prior_probability_table

    prior_probability_table = {}


    for key, value in bigram_likelihood_table.iteritems():
        current_pos = key[1]

        if current_pos not in prior_probability_table:
            prior_probability_table[current_pos] = {}

            for key, value in bigram_likelihood_table.iteritems():
                    if key[1] == current_pos:
                        prior_probability_table[current_pos][key] = value


    # HMM POS Tagging

    output = []
    with open("development_set.txt", "r+") as f:
        line_counter = 0
        appends = 0

        for line in f:

            word = line.rstrip()

            if line_counter == 0:
                most_likely_first = max(likelihood_table.iteritems(), key=operator.itemgetter(1))[0]
                output.append([word, most_likely_first])
                appends+=1

            else:
                try:
                    if len(likelihood_table_words[word]) == 1:
                        # assign it as the next pos
                        pos = likelihood_table_words[word].keys()[0]
                        output.append([word, pos])
                        appends+=1

                    #there are multiple occurences of this word as different POS tags
                    elif len(likelihood_table_words[word]) > 1:
                        # find the highest probability given the last POS tag: i.e.
                        # for each of the POS tags this word appears as, multiply it by the prior probability including the last POS tag
                        # and return the highest number.
                        previous_pos_tag = output[len(output)-1][1]

                        max_val = 0
                        max_combination = []

                        for key, value in likelihood_table_words[word].iteritems():
                            check_max = calculate_max(key, value, previous_pos_tag, prior_probability_table)

                            if check_max[1] > max_val:
                                max_val = check_max[1]
                                max_combination = check_max

                        # max_combination contains the POS tag to add to output
                        output.append([word, max_combination[0]])
                        appends+=1

                except:
                    # use POS likelihood_table
                    previous_pos_tag = output[len(output)-1][1]

                    max_val = 0
                    max_combination = []

                    for key, value in likelihood_table.iteritems():
                        check_max_exception = calculate_max_exception(key, value, previous_pos_tag, prior_probability_table)

                        if check_max_exception[1] > max_val:
                            max_val = check_max_exception[1]
                            max_combination = check_max_exception


                    output.append([word, max_combination[0]])
                    appends+=1

            line_counter+=1

        print line_counter, " lines read."
        print appends, " POS's appended to output"

def calculate_max_exception(k, v, previous_pos_tag, prior_probability_table):
    pos_document_probability = v
    pos = k

    search_key = (previous_pos_tag, pos)
    try:
        max_val = pos_document_probability * prior_probability_table[pos][search_key]
    except:
        max_val = pos_document_probability

    return [pos, max_val]


def calculate_max(k, v, previous_pos_tag, prior_probability_table):

    likelihood_probability = v
    pos = k
    search_key = (previous_pos_tag, pos)

    max_val = likelihood_probability * prior_probability_table[pos][search_key]
    return [pos, max_val]

main()
