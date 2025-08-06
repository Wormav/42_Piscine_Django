from django.shortcuts import render

import os
from datetime import datetime
from django.conf import settings
from .forms import HistoryForm

def history_view(request):
	form = HistoryForm()
	history_entries = []

	# Load history from the log file
	if os.path.exists(settings.LOG_FILE_PATH):
		with open(settings.LOG_FILE_PATH, 'r', encoding='utf-8') as f:
			for line in f:
				if line.strip():
					history_entries.append(line.strip())

	if request.method == 'POST':
		form = HistoryForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']
			timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			entry = f"{timestamp} - {text}"

			# Create the directory if it does not exist
			os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)

			# Append the entry to the log file
			with open(settings.LOG_FILE_PATH, 'a', encoding='utf-8') as f:
				f.write(entry + '\n')

			# Add the entry to the displayed history
			history_entries.append(entry)

			# Reset the form
			form = HistoryForm()

	return render(request, 'form.html', {
		'form': form,
		'history_entries': history_entries
	})
