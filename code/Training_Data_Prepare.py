import os
import sys
import commands
import numpy as np
import time
import math
import multiprocessing as mp
import random

nn = "\n"
tt = "\t"
ss = "/"
cc = ","

def main(argElm):
	#Step_3_1: Collecting positive examples
	messageStr = "Step_3_1: Collecting positive examples..."
	ClockAndReport_func(messageStr)
	CollectPositives_func(argElm)

	#Step_3_2: Collecting negative examples
	messageStr = "Step_3_2: Collecting negative examples..."
	ClockAndReport_func(messageStr)
	CollectNegatives_func(argElm)

	#Step_3_3: Organizing training dataset
	messageStr = "Step_3_3: Organizing training dataset..."
	ClockAndReport_func(messageStr)
	OrganizeTraiData_func(argElm)

	##End main

def OrganizeTraiData_func(argElm):
	outPrefix = argElm.Out_Prefix_str
	trainDir = "%s.TrainDir"%outPrefix
	modelDir = "%s.ModelDir"%outPrefix	
	makePath(modelDir)

	posExample_path = trainDir + ss + "Positive.RDD.RawList.txt"
	negExample_path = trainDir + ss + "Negative.RDD.RawList.txt"

	posCsv_path = trainDir + ss + "Positive.RddList.csv"
	negCsv_path = trainDir + ss + "Negative.RddList.csv"
	
	posSize_int = ListToCsv_sub(posExample_path, posCsv_path, "Positive")
	negSize_int = ListToCsv_sub(negExample_path, negCsv_path, "Negative")
	trainMax_int = int(argElm.Train_MaxLimit_int)
	optimalSize_int = min([posSize_int, negSize_int, trainMax_int])

	trainList_path = modelDir + ss + "Train.RddList.csv"
	ResizingCsv_sub(posCsv_path, negCsv_path, optimalSize_int, trainList_path)

	logFile_path = "%s.Step3.Training.Data.Log"%outPrefix
	logFile = open(logFile_path, 'w')
	logFile.write("Positive-examples: %s sites"%posSize_int + nn)
	logFile.write("Negative-examples: %s sites"%negSize_int + nn)
	logFile.write("Balanced training-set size: %s sites"%(optimalSize_int*2) + nn)
	logFile.close()

	rmCmd = "rm -r %s"%trainDir
	commands.getoutput(rmCmd)
	##End OrganizeTraiData_func

def ResizingCsv_sub(posCsv_path, negCsv_path, optimalSize_int, trainList_path):
	featTag_line = makeLine(FeatureTag_list + ["TrainLabel"], cc)
	trainFile = open(trainList_path, 'w')
	trainFile.write(featTag_line + nn)
	trainFile.close()

	a, b, c = optimalSize_int, posCsv_path, trainList_path
	ShuffleFile_sub(posCsv_path, trainList_path, optimalSize_int, 'a')

	a, b, c = optimalSize_int, negCsv_path, trainList_path
	ShuffleFile_sub(negCsv_path, trainList_path, optimalSize_int, 'a')
	##End ResizingCsv_sub

def ShuffleFile_sub(inFile_path, outFile_path, shufSize_int, writeMode_bit):
	lineNum_int = sum(1 for line in open(inFile_path))
	pickNum_int = min(lineNum_int, shufSize_int)
	pickedIdx_list = random.sample(range(lineNum_int), pickNum_int)

	outFile = open(outFile_path, writeMode_bit)	
	inIdx = 0
	for inLine in open(inFile_path):
		if inIdx in pickedIdx_list:
			outFile.write(inLine.strip() + nn)
			##End if
			
		inIdx += 1
		##End for
	outFile.close()
	##End ShuffleFile_sub

FeatureTag_list = ["ReadDepth", "VAF", "CallQual", "FQ", "SGB", "MQ", "MQB", "MQ0F", "BQB", "VDB", "RPB", "PV1", "PV2", "PV3", "PV4"]
def ListToCsv_sub(examplePath, csvPath, trainLabel):
	exampleFile = open(examplePath, 'r')
	csvFile = open(csvPath, 'w')
	lineCounter = 0

	while True:
		exampleLine = exampleFile.readline()
		if not exampleLine:
			break
			##End if

		try:
			posTag, samQual, featLine = exampleLine.split()
		except:
			continue
			##End try-except	

		featDic = {}
		for featElm in featLine.split(";"):
			try:
				featTag, featVal = featElm.split("=")
			except:
				continue
				##End try-except

			featDic[featTag] = featVal
			##End for

		try:
			featDic["ReadDepth"] = featDic["DP"]
			featDic["CallQual"] = float(samQual)
			a, b, c, d = map(float, featDic["DP4"].split(cc))
			vafVal = (c+d)/(a+b+c+d)
			featDic["VAF"] = vafVal
			a, b, c, d = map(float, featDic["PV4"].split(cc))
			for i in range(1, 5):
				featDic["PV%s"%i] = [a, b, c, d][i-1]
				##End for
			featVal_list = map(lambda x:round_figures(featDic[x]), FeatureTag_list) 
		except:
			continue
			##End try-except
	
		featVal_line = makeLine(featVal_list + [trainLabel], cc)
		csvFile.write(featVal_line + nn)
		lineCounter += 1
		##End while

	csvFile.close()
	return lineCounter
	##End ListToCsv_sub

def round_figures(x): 
	y = float("%.5f"%float(x))
	return y		
	##End round_figures


def CollectNegatives_func(argElm):
	outPrefix = argElm.Out_Prefix_str
	rawList_path = "%s.RDD.RawList.txt"%outPrefix
	negList_path = argElm.Neg_SiteList_path
	
	trainDir = "%s.TrainDir"%outPrefix
	makePath(trainDir)	

	negSiteList_path = trainDir + ss + "Negative.SiteList.txt"
	a, b = negList_path, negSiteList_path
	SiteSort_sub(negList_path, negSiteList_path)

	negExample_path = trainDir + ss + "Negative.RDD.RawList.txt"
	a, b, c = rawList_path, negSiteList_path, negExample_path
	SiteJoin_sub(rawList_path, negSiteList_path, negExample_path)
	##End CollectPositives_func

def SiteJoin_sub(rawList_path, refList_path, outList_path):
	commands.getoutput("join %s %s > %s"%(rawList_path, refList_path, outList_path))
	##End SiteJoin_sub

def SiteSort_sub(inSite_path, outSite_path):
	#[1]
	outPre_path = outSite_path + ".pre"
	outPre_file = open(outPre_path, 'w')
	for inSite_line in open(inSite_path):
		chrId, varPos, refNuc, varNuc = inSite_line.split()
		varPos_line = "%s.%s.%s:%s"%(chrId, varPos, refNuc.upper(), varNuc.upper())
		outPre_file.write(varPos_line + nn)
		##End for
	outPre_file.close()
	#[2]
	sortCmd = "sort -k1,1 %s > %s; rm %s"%(outPre_path, outSite_path, outPre_path)
	commands.getoutput(sortCmd)
	##End SiteSort_sub

def CollectPositives_func(argElm):
	outPrefix = argElm.Out_Prefix_str
	rawList_path = "%s.RDD.RawList.txt"%outPrefix
	posList_path = argElm.Pos_SiteList_path
	
	trainDir = "%s.TrainDir"%outPrefix
	makePath(trainDir)	

	posSiteList_path = trainDir + ss + "Positive.SiteList.txt"
	a, b = posList_path, posSiteList_path
	SiteSort_sub(posList_path, posSiteList_path)

	posExample_path = trainDir + ss + "Positive.RDD.RawList.txt"
	a, b, c = rawList_path, posSiteList_path, posExample_path
	SiteJoin_sub(rawList_path, posSiteList_path, posExample_path)
	##End CollectPositives_func

import datetime as dt
def ClockAndReport_func(messageStr):
	currentTime = dt.datetime.now()
	print "%s [%s]"%(messageStr, currentTime)
	##End ClockAndReport_func


def GetNumString_func(sampleNum, sampleSize):
	decNum = int(math.log(sampleSize, 10)) + 1
	numString = str(sampleNum)
	while len(numString) < decNum:
		numString = "0" + numString
		##End while

	return numString
	##End GetNumString_func

def makePath(dirPath):
	return commands.getoutput("mkdir %s"%dirPath)
	##End makePath

def makeLine(tokenList, sepToken):
	return sepToken.join(map(str, tokenList))	
	##End makeLine

if __name__ ==  "__main__" :
	main()
	sys.exit()
