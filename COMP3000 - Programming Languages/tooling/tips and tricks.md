# How to run

    > ruby split_out.rb; ruby xml_from_yaml.rb; ruby fill_imgs.rb

# How to use

  * Put a level 1 for each learning outcome in your topic
  * Put a level 2 heading for each venue (class, exam, etc) under each learning outcome

You now have a map of what you need to fill out to generate good question coverage.  You can use the outline view to see the overall shape of the document

You can now make up questions for each learning outcome and venue.  Use a level 3 heading for the name of the question and then all the lines below that are in the question format.  Question formats are:
  * gift
  * yaml-by-matt

Gift questions use the [standard gift formatting](https://docs.moodle.org/404/en/GIFT_format) including all its warts.

### Gift tips
  * no blank lines!
  * use <pre> and start each line with | for code
  * remember to escape =,{,},~ in code blocks

### Yaml-by-matt
Is used as an input format for questions that will end up in XML.  The question name should include <questiontype> at the end.  I make up question types as I go.

# What is happening?

`split_out.rb` takes a markdown-ish file and splits out each heading.  Heading level 1 is treated as a learning outcome, level 2 is a venue for the question to appear in and level 3 is the question name.  As well as this, any definitions at the top level are glossary terms.  After running this you will have:
  * glossary file (complete)
  * gift file (complete)
  * yaml file (ready for next step)

`xml_from_yaml.rb` will use the templates to fill out the moodle xml for each question type and generate the xml file

`fill_imgs.rb` will look for any image tags and embed the base64 encoding of the image so no attachments are needed.

# YAML-by-matt question types

## <essay>
Gift format doesn't let you include a sample answer, so we do these via xml.  Fields are:
  * question
  * answer

## <lox>
CodeRunner questions for lox programs.  Fields are:
  * question
  * answer
  * tests (which is an array of key, values where key is the code to run the test, value is the output of the test)

## images in gift answers
These need to have all the `=` and `~` escaped, so there is an alternative `<img src=`form to use.  Put a slash before `=` as in `<img src\="jfdjkl` and all the changes required for gift answer fields will work