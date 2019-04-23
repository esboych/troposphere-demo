from troposphere import Template
from creator import stack
from os import path

ENV_LIST = ['Development', 'Experimental', 'Production']

def main():
    """ Creating three empty Template objects and pass each to create_template()
    as argument along with the corresponding environment type of
    ['Development', 'Experimental', 'Production'] """
    for env in ENV_LIST:
        template = stack.create_template(Template(), env)

        # printing out the completed template
        print("Resulting json: \n\n%s" % template.to_json())

        # writing template to the file
        template_file_name = "".join(("template-", str.lower(env), ".json"))
        template_file_name = path.join("templates", template_file_name)
        with open(template_file_name, 'w+') as fd:
            # adding newline here to ensure it's text file
            fd.write("".join((template.to_json(), "\n")))

if __name__ == '__main__':
    main()

