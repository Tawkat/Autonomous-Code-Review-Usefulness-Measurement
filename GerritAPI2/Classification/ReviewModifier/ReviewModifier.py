from Classification.ReviewModifier.FileCount import FileCount
from Classification.ReviewModifier.LineNo import LineNo
from Classification.ReviewModifier.NitPickingCount import NitPickingCount
from Classification.ReviewModifier.PatchSet import PatchSet
from Classification.ReviewModifier.PosNegWordCount import PosNegWordCount
from Classification.ReviewModifier.QuestionMark import QuestionMark
from Classification.ReviewModifier.WordCount import WordCount
from Classification.ReviewModifier.ProgWordCount import ProgWordCount


class ReviewModifier:

    def __init__(self,review,isLast=0):
        self.review=review.lower()
        self.isLast=isLast

        self.wordCount=WordCount(self.review)
        self.lineNo=LineNo(self.review)
        self.progWordCount=ProgWordCount(self.review)
        self.fileCount=FileCount(self.review)
        self.questionMark=QuestionMark(self.review)
        self.patchSet=PatchSet(self.review)
        self.posNegWordCount=PosNegWordCount(self.review)
        self.nitCount=NitPickingCount(self.review)

    def getReviewModifier(self):

        wc=self.wordCount.getWordCount()
        ln=self.lineNo.getLineNo()
        pwc=self.progWordCount.getProgWordCount()
        fm=self.fileCount.getFileCount()
        qm=self.questionMark.getQuestionMark()
        pWord,nWord=self.posNegWordCount.getPosNegWordCount()
        nc=self.nitCount.getNitCount()

        sampleList=[[fm,wc,ln,pwc,qm,pWord,nWord,nc,self.isLast]]
        #print("Sample List: %s" % sampleList)
        return sampleList

'''
if __name__=='__main__':
    print(rm.getReviewModifier())

'''