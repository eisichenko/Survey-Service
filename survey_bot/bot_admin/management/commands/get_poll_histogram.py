from django.core.management.base import BaseCommand
from bot_admin.models import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class Command(BaseCommand):
    help = 'Get histogram of a specific poll'
    
    def handle(self, *args, **kwargs):
        print()
        
        try:
            poll_group_id = int(input('Enter poll group id (you can find it in "list_polls" command): '))
            polls = TelegramPoll.objects.filter(poll_group_id=poll_group_id).all()
            
            if len(polls) == 0:
                raise Exception('Poll group was not found')
            
            total_answers = len(polls)
            
            print('Was chosen')
            print(f'Poll group ID: {polls[0].poll_group_id}; Question: {polls[0].question}; Time (UTC): {polls[0].created_at}; ' + 
                  f'Correct answers: {polls[0].correct_options}; Option number: {polls[0].option_number}\n')
            
            answers_number = [[i + 1, 0] for i in range(polls[0].option_number)]
            
            for poll in polls:
                poll: TelegramPoll
                selected_answers = poll.selected_options
                
                if selected_answers != None:
                    for i in selected_answers:
                        answers_number[i][1] += 1
                    
            print(answers_number)
            
            options = [f'#{answer[0]}' for answer in answers_number]
            options_pos = list(range(len(options)))
            
            percentages = [(answer[1] / float(total_answers)) for answer in answers_number]
            answer_numbers = [answer[1] for answer in answers_number]
            
            print("\nStats:\n")
            
            for i in range(len(options)):
                print(f'{options[i]}: {answer_numbers[i]}/{total_answers} answers ({percentages[i] * 100.0 : 0.2f}%)')
            
            choice = input('\nWould you like to see histogram of answers? (y/n)')
            
            if choice == 'y':
                plt.figure(figsize=(10, 7), num='Histogram')
                plt.title('Result histogram', pad=30.0)
                plt.xlabel('Option number', labelpad=5.0)
                plt.ylabel('Percentage', labelpad=20.0)
                plt.ylim([0.0, 1.0])
                
                plt.bar(options_pos, 
                        percentages,
                        color=('blue', 'green', '#f00', '#990099', '#0f0', '#ff0', '#0ff', '#9C3131', '#808080', '#03ACFF'),
                        width=0.5)
                
                for i, v in enumerate(percentages):
                    plt.text(options_pos[i], v + 0.01, f'{percentages[i] * 100.0 : .2f}%', horizontalalignment="center")
                
                plt.xticks(list(range(len(options))), options)
                plt.show()
            
        except Exception as e:
            print(e)
            return
        
        print()
