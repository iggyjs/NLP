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
            value = value.lower()

            if not pos in count_table:
                count_table[pos]= 1
                total_pos_tags += 1

            if pos in count_table:
                count_table[pos] += 1
            total_words += 1

        print "Total words in corpus: " , total_words

        # likelihood_table population
        for key, value in count_table.iteritems():
            likelihood_table[key] = float(count_table[key])/total_words


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

main()
