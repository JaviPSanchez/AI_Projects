# https://github.com/feder-cr/linkedIn_auto_jobs_applier_with_AI


# Run the Bot:

# Dynamic Resume Generation: If you don't use the --resume option, the bot will
# automatically generate a unique resume for each application. This feature uses
# the information from your plain_text_resume.yaml file and tailors it to each
# specific job application, potentially increasing your chances of success by
# customizing your resume for each position.

python main.py


# Using a Specific Resume: If you want to use a specific PDF resume for all applications
# , place your resume PDF in the data_folder directory and run the bot with the --resume option:


python main.py --resume ./assets/Data_Engineer_Javier_Palomino.pdf


