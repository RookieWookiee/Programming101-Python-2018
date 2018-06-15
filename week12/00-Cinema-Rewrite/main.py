from views import cli_framework as poormans_click
import views.commands.cli 



from views.commands.cli import login
login(username='test', password='Testtest!')
poormans_click.start_repl()
