from General import General;
import os;

class ConfigCreator (General):
	def __init__ (self):
		self.questions = [
			{
				"question": "Source folder:",
				"id": "src",
				"key": "folder"
			},
			{
				"question": "Destination folder:",
				"id": "dest",
				"key": "destination"
			},
			{
				"question": "Search criteria:",
				"id": "searchC",
				"key": "nameCriteria"
			},
			{
				"question": "Is there a RegEx code in the search criteria? (y/n)",
				"id": "regexInSearchC",
				"key": "nameCriteriaRegex"
			},
			{
				"question": "Is the search criteria case sensitive (y/n)",
				"id": "case",
				"key": "ignoreCase"
			},
			{
				"question": "Search criteria extension:",
				"id": "searchE",
				"key": "extension"
			},
			{
				"question": "Search criteria prefix:",
				"id": "searchP",
				"key": "prefix"
			},
			{
				"question": "Episode search criteria:",
				"id": "episodeS",
				"key": "episodeCriteria"
			},
			{
				"question": "Match season? (y/n)",
				"id": "seasonM",
				"key": "matchSeason"
			},
			{
				"question": "Season search criteria:",
				"id": "seasonS",
				"key": "seasonCriteria"
			},
			{
				"question": "Renaming title:",
				"id": "renameT",
				"key": "nameLeader"
			},
			{
				"question": "Rename safely? (y/n)",
				"id": "renameS",
				"key": "renameSafely"
			},
			{
				"question": "Config file name:",
				"id": "configN",
				"key": "name"
			}
		];

	def askQuestion(self, id, saveData = {}):
		for questionGroup in self.questions:
			if not questionGroup["id"] == id:
				continue;

			userInput = input(questionGroup["question"] + "  ");

			if id in ["src", "dest"]:
				if not os.path.isdir(userInput):
					if id == "src":
						print("Invalid source folder!");
						saveData = self.askQuestion("src", saveData);
					else:
						print("Invalid destination folder!");
						saveData = self.askQuestion("dest", saveData);
				elif not os.path.isabs(userInput):
					print("Absolute paths only!");
					if id == "src":
						saveData = self.askQuestion("src", saveData);
					else:
						saveData = self.askQuestion("dest", saveData);
				else:
					saveData[questionGroup["key"]] = userInput;
			elif id == "searchC":
				if userInput == "":
					print("Please input a valid search criteria!");
					saveData = self.askQuestion("searchC", saveData);
				else:
					saveData[questionGroup["key"]] = userInput;
			elif id == "regexInSearchC":
				if userInput in ["", "n"]:
					saveData[questionGroup["key"]] = False;
				elif userInput == "y":
					saveData[questionGroup["key"]] = True;
				else:
					print("Invalid entry!");
					saveData = self.askQuestion("regexInSearchC", saveData);
			elif id == "case":
				if userInput in ["", "n"]:
					saveData[questionGroup["key"]] = False;
				elif userInput == "y":
					saveData[questionGroup["key"]] = True;
				else:
					print("Invalid entry!");
					saveData = self.askQuestion("case", saveData);
			elif id == "searchP" or id == "searchE":
				saveData[questionGroup["key"]] = userInput;
			elif id == "episodeS":
				if userInput == "":
					print("Please input a valid episode search criteria!");
					saveData = self.askQuestion("episodeS", saveData);
				else:
					saveData[questionGroup["key"]] = userInput;
			elif id == "seasonM":
				if userInput == "" or userInput == "n":
					saveData[questionGroup["key"]] = False;
				elif userInput == "y":
					saveData[questionGroup["key"]] = True;
				else:
					print("Invalid entry!");
					saveData = self.askQuestion("seasonM", saveData);
			elif id == "seasonS":
				if userInput == "" and saveData["matchSeason"]:
					print("Please input a valid season search criteria!");
					saveData = self.askQuestion("seasonS", saveData);
				else:
					saveData[questionGroup["key"]] = userInput;
			elif id == "renameT":
				if userInput == "":
					print("Please input a valid renaming title!");
					saveData = self.askQuestion("renameT", saveData);
				else:
					saveData[questionGroup["key"]] = userInput;
			elif id == "renameS":
				if userInput == "" or userInput == "n":
					saveData[questionGroup["key"]] = False;
				elif userInput == "y":
					saveData[questionGroup["key"]] = True;
				else:
					print("Invalid entry!");
					saveData = self.askQuestion("renameS", saveData);
			elif id == "configN":
				if userInput == "":
					print("Please input a valid name for the config file!");
					saveData = self.askQuestion("configN", saveData);
				elif os.path.isfile("./configs/%s.json" % userInput):
					print("Name already taken!");
					saveData = self.askQuestion(questionGroup["id"], saveData);
				else:
					saveData[questionGroup["key"]] = userInput;
			else:
				print("Invalid question id!");

			return saveData;

	def askUserInput (self):
		saveData = {};
		for questionGroup in self.questions:
			saveData = self.askQuestion(questionGroup["id"], saveData);
		
		return saveData;

	def confirmSaveConfigFile(self, saveData):
		print("\n%s" % self.unjsonize(saveData));
		userInput = input("\nAre you sure you want to save this config? (y/n)  ");
		if userInput in ["", "n"]:
			print("Exiting...");
			self.wait(3);
		elif userInput == "y":
			print("Saving...");

			saveData["newExtension"] = False;
			saveData["seasonLeader"] = " season ";
			saveData["episodeLeader"] = " episode ";

			self.save_json(f'./configs/{saveData["name"]}.json', saveData);
			self.wait(3);
		else:
			print("Invalid response!");
			self.confirmSaveConfigFile(saveData);

if __name__ == '__main__':
	creator = ConfigCreator();
	data = creator.askUserInput();
	creator.confirmSaveConfigFile(data);