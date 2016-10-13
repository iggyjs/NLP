def main():


    # wrong
    # likelihood_table should be the appearance of some POS tag as a word over all of the occurences of that specific POS tag

    count_table = {}
    total_words = 0

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

            if pos in count_table:
                count_table[pos] += 1

            total_words += 1

        print "Total words in corpus: ", total_words

        
    """
    likelihood_table = {}


    counter = 0;
    for word, pos in count_table.iteritems():
        total_count = 0
        likelihood_table[word] = {}

        for this_pos, pos_total in pos.iteritems():
            total_count += pos_total

        for this_pos, count in pos.iteritems():
            likelihood_table[word][this_pos] = float(pos_total)/total_count;
            print word, likelihood_table[word];


        for i, count in pos.iteritems():
            likelihood_table[word] = float(count)/total_count


    for key, value in likelihood_table.iteritems():
        print key, value

    prior_probability_table = {}

    """
main()
