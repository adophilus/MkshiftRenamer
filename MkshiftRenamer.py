import sys
import os
import subprocess as sp
from General import General

class FileRenamer (General):
	def __init__(self):
		self.configs = []

		self.loadConfigs()


	def loadConfigs(self):
		fileList = os.listdir("./configs/")

		if len(fileList) == 0:
			return [False, "There are no configurations to work with!"]

		for configFile in fileList:
			config = self.load_json(f"./configs/{configFile}")
			self.configs.append(config)

	def prepareRenameList(self, configName):
		for config in self.configs:
			# print(configName)
			if config["name"] != configName:
				continue

			if not os.path.isdir(config["folder"]):
				return [False, "Invalid source folder!"]

			if not os.path.isdir(config["destination"]):
				return [False, "Invalid destination folder!"]

			if not os.path.isabs(config["folder"]):
				return [False, "Only absolute paths are allowed!"]


			files = os.listdir(config["folder"])

			if len(files) == 0:
				return [False, "There are no files in this directory"]

			retList = []
			safetyFolder = False
			for file in files:
				file = os.path.join(config["folder"], file)

				if os.path.isdir(file):
					# files.remove(os.path.dirname(file))
					continue

				# print(file)
				filePath = os.path.join(config["folder"], file)

				if not config["ignoreCase"] and config["nameCriteria"] not in file and not config["nameCriteriaRegex"]:
					continue

				if config["ignoreCase"] and not self.searchString(file, config["nameCriteria"], ignoreCase = True):
					continue

				if not self.searchString(file, f'^{config["prefix"]}'):
					continue

				if not self.searchString(file, f'{config["extension"]}$'):
					continue

				if config["matchSeason"]:
					seasonNumber = self.searchString(file, config["seasonCriteria"])
					if not seasonNumber:
						continue

					# seasonNumber = self.searchString(seasonNumber, "(\\d+)")
					seasonNumber = seasonNumber[1]

				episodeNumber = self.searchString(file, config["episodeCriteria"])
				if not episodeNumber:
					continue
				episodeNumber = episodeNumber[0]

				if config["matchSeason"]:

					newName = "{nl}{sl}{sn}{el}{en}{ext}".format(
						nl = config["nameLeader"],
						sl = config["seasonLeader"],
						sn = seasonNumber,
						el = config["episodeLeader"],
						en = episodeNumber,
						ext = config["extension"]
					)

				else:

					newName = "{nl}{el}{en}{ext}".format(
						nl = config["nameLeader"],
						el = config["episodeLeader"],
						en = episodeNumber,
						ext = config["extension"]
					)

				newName += config["newExtension"] or config["extension"]
				if config["renameSafely"]:
					safetyFolder = os.path.join(config["destination"], "safety-folder")
					newFilePath = os.path.join(safetyFolder, os.path.basename(newName))
					# print(newFilePath)
				else:
					newFilePath = os.path.join(config["destination"], os.path.basename(file))

				retList.append([file, newFilePath])

			return {"retList": retList, "safetyFolder": safetyFolder}

	def getRenameList (self, config):
		for config in self.configs:
			if config["name"] != config:
				continue
			
			return self.prepareRenameList(config)

	def getRenameListAll(self):
		if len(self.configs) == 0:
			return [False, "No config file available!"]

		return [
		    self.prepareRenameList(config["name"])["retList"]
		    for config in self.configs
		]

	def finalize(self, array):
		renameSafely = False
		# print(array[0][1])
		# return False
		if os.path.basename(os.path.dirname(
		    array[0][1])) == "safety-folder" and not os.path.isdir(
		        os.path.dirname(array[0][1])):
			renameSafely = True
			os.mkdir(os.path.dirname(array[0][1]))

		for [old, new] in array:
			if renameSafely:
				print("Copying {old} to {new}".format(old = old, new = new))
				sp.check_call(["cp", old, new])
			else:
				print("Renaming {old} to {new}".format(old = old, new = new))
				os.rename(old, new)

if __name__ == '__main__':
	renamer = FileRenamer()

	renamingList = renamer.getRenameListAll()
	for rename in renamingList:
		renamer.finalize(rename)