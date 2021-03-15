#!/usr/bin/env python3

from sys import stdout, stderr, exit, argv
from os import environ
from os.path import join, split

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor on your local machine.)", file=stderr)

err_ruamel = None
yaml_is_installed = True
try:
    import ruamel.yaml
except Exception as e:
    yaml_is_installed = False
    err_ruamel = e

            
class Env:
    def __init__(self, problem, service, args_list):
        self.service_server_fullname = argv[0]
        self.exe_path = split(argv[0])[0]
        self.meta_dir = environ["TAL_META_DIR"]
        self.problem = problem
        self.service = service
        self.args_list = args_list
        self.arg = {}
        for name, val_type in args_list:
            if val_type == str:
                self.arg[name] = environ[f"TAL_{name}"]
            elif val_type == bool:
                self.arg[name] = (environ[f"TAL_{name}"] == "1")
            elif val_type == int:
                self.arg[name] = int(environ[f"TAL_{name}"])
            elif val_type == float:
                self.arg[name] = float(environ[f"TAL_{name}"])
            else:
                for out in [stdout, stderr]:
                    print(f"# Unrecoverable Error: type {val_type} not yet supported in args list (the set of supported types can be extended by communities of problem makers adding further elif clauses here above). Used to interpret arg {name}.", file=out)
                exit(1)
    def __getitem__(self, key):
        return self.arg.get(key)


class Lang:
    def __init__(self, ENV, TAc, myfeval, book_required=False):
        self.myfeval = myfeval
        self.ENV=ENV
        self.TAc=TAc
        self.messages_book = None
        self.messages_book_file = join(ENV.meta_dir, ENV.exe_path, ENV.service + "_feedbackBook." + ENV['lang'] + ".yaml")
        if not yaml_is_installed:
            if book_required:
                for out in [stdout, stderr]:
                    TAc.print("Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine):", "red", ["bold"])
                    print(f" the service {ENV.service} you required strongly relies on a .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated. I close the channel.", file=out)
                exit(1)
            else:
                TAc.print("# Recoverable Error: ", "red", ["bold"], end="", file=stderr)
                print(err_ruamel, file=stderr)
                print("# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue (as long as you can understand the little needed English).\n# (To enjoy a feedback in a supported language install the python package 'ruamel'. The languages supported by a problem service appear as the options for the lang parameter listed by the command `rtal list`)", file=stderr)
        else:
            try:
              print(f"self.messages_book_file={self.messages_book_file}")
              with open(self.messages_book_file, 'r') as stream:
                try:
                    yaml_book = ruamel.yaml.safe_load(stream)
                    self.messages_book = yaml_book
                except yaml.YAMLError as exc:
                    if book_required:
                        for out in [stdout, stderr]:
                            TAc.print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine):", "red", ["bold"])
                            TAc.print(f" the messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file).", "red", ["bold"])
                            print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires this .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated.", file=out)
                            print(exc, file=out)
                        exit(1)
                    else:
                        TAc.print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file).", "red", ["bold"], file=stderr)
                        print(exc, file=stderr)
                        print(f"# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
            except IOError as ioe:
                if book_required:
                    for out in [stdout, stderr]:
                        TAc.print(f"Internal error (please, report it to those responsible): The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.", "red", ["bold"])
                        print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires to have access to this .yaml file.", file=out)
                        print(ioe, file=out)
                    exit(1)
                else:
                    TAc.print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.", "red", ["bold"], file=stderr)
                    print(ioe, file=stderr)
                    print(f"# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
        self.opening_msg = self.render_feedback("open-channel",f"# I will serve: problem={ENV.problem}, service={ENV.service}")
        for arg_name, _ in ENV.args_list:
            arg_val = ENV[arg_name]
            self.opening_msg += f", {arg_name}={arg_val}"
        if self.messages_book == None:
            self.opening_msg += f".\n# The feedback_source is the one hardcoded in the service server ({ENV.service_server_fullname})"
        else:
            self.opening_msg += f".\n# The feedback_source is the dictionary of phrases yaml file ({self.messages_book_file}) in the service server folder."
        TAc.print(self.opening_msg, "yellow", ["underline"], file=stderr)


    def render_feedback(self, msg_code, msg_English_rendition):
        if self.messages_book != None and msg_code not in self.messages_book:
            print(f"Warning to the problem maker: the msg_code={msg_code} is not present in the selected messages_book")
        if self.messages_book == None or msg_code not in self.messages_book:
            return msg_English_rendition
        return self.myfeval(self.messages_book[msg_code])



class TALcolors:
    def __init__(self, ENV):
        self.numNO = 0
        self.numOK = 0
        self.colored_print = ENV["ISATTY"] and termcolor_is_installed

    def print(self, msg_text, *msg_rendering, **kwargs):
      if type(msg_rendering[-1]) == list:
          msg_style = msg_rendering[-1]
          msg_colors = msg_rendering[:-1]
      else:
          msg_style = []
          msg_colors = msg_rendering
      if self.colored_print:
          print(colored(msg_text, *msg_colors, attrs=msg_style), **kwargs)
      else:
          print(msg_text, **kwargs)

    def NO(self):
        self.numNO += 1
        self.print("No! ", "red", ["blink", "bold"], end="")

    def OK(self):
        self.numOK += 1
        self.print("OK! ", "green", ["bold"], end="")

    def GotBored(self):
        self.print("! (I got bored)", "white")

    def Finished(self):
        self.print(f"! (We have finished) Correct answers: {self.numOK}/{self.numOK+self.numNO}", "white")
