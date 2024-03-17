BAR_LENGTH = 64

def display(progress, total):
	progress_count = int(BAR_LENGTH * (progress / total))
	bar = chr(9608) * progress_count + chr(9617) * (BAR_LENGTH - progress_count)
	print(f"\r|{bar}| {100 * progress / total:.2f}%", end="\r")
	if progress == total:
		print("")

