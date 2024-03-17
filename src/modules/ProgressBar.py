import math

BAR_LENGTH = 64


class ProgressBar:
	def __init__(self, total):
		self.total = total
		self.progress = 0

	## Displays the progress bar if the new percentage has been incremented by at least 1
	def update_and_display(self, new_progress):
		old_percentage = self.get_percentage()
		self.progress = new_progress

		if math.floor(self.get_percentage()) - math.floor(old_percentage) >= 1:
			self.display()


	def display(self):
		bar = self.get_bar_text()
		print(f"\r|{bar}| {self.get_percentage():.1f}%", end="\r")
		if self.progress == self.total:
			print("")


	## Input: Toggle between percentage and raw value 'percent'
	def get_percentage(self, percent=True):
		value = self.progress / self.total
		if percent:
			return 100 * value
		return value


	## Gets the visualized progress bar string
	def get_bar_text(self):
		bar_count = int(self.get_percentage(percent=False) * BAR_LENGTH)
		return chr(9608) * bar_count + chr(9617) * (BAR_LENGTH - bar_count)
