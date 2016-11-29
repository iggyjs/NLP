import nltk
grammar = nltk.CFG.fromstring("""
    S -> S S
    S -> NP VP | NP PP
    PP -> IN NP

    NP -> Det JJ NNS | Det NN | NNS | NP PP
    VP -> VBD IN | VPB PP | VBD

    NNS -> 'Scientists'
    VBD -> 'think'
    IN -> 'that'


    Det -> 'any'
    JJ -> 'habitable'
    NNS -> 'areas'

    PP -> IN Det NN | IN Det NN NN
    IN -> 'on'
    Det -> 'the'
    NN -> 'planet'

    VPB -> 'are'

    IN -> 'in'
    Det -> 'the'
    NN -> 'border'
    NN -> 'region'

""")
sent = ['Scientists','think', 'that', 'any', 'habitable', 'areas', 'on', 'the', 'planet', 'are', 'on', 'the', 'border', 'region']
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
	print(tree)
