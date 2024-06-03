from leetscrape import GetQuestionsList, GetQuestion

qi = GetQuestion(titleSlug="count-triplets-that-can-form-two-arrays-of-equal-xor")
oko=qi.scrape()
from leetscrape import GenerateCodeStub

fcs = GenerateCodeStub(qid=qi.questions_info['QID']['count-triplets-that-can-form-two-arrays-of-equal-xor'])
fcs.generate()

from leetscrape import ExtractSolutions
es = ExtractSolutions("q_1442_countTripletsThatCanFormTwoArraysOfEqualXor.py")
sols = es.extract()
es.to_mdx("q_1442_countTripletsThatCanFormTwoArraysOfEqualXor.md")