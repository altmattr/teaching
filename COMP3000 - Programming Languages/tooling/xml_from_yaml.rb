require_relative 'templates.rb'
require 'yaml'

build_dir = "../build"
Dir.glob("#{build_dir}/*.yaml") do |filename| 
    puts filename
    week = filename[/\.\.\/build\/(.*)\..*/,1]
    output = "xml"
    puts week
    category = ""
    questions = YAML.load_stream(File.read(filename))
    File.open("#{build_dir}/#{week}_questions.xml", "w") {|io| io.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><quiz>")}
    questions.each do |question|
            if question.key?("category") then
                category = question["category"]
                File.open("#{build_dir}/#{week}_questions.xml", "a+") do |io| 
                io.write(xml_category(category))
                io.write("\n\n")
                end
            else
                puts "  #{question["title"]}"
                case question["type"]
                in "lox"
                    File.open("#{build_dir}/#{week}_questions.xml", "a+") do |io| 
                        io.write(lox_question_top(question["title"],
                                                  question["question"], 
                                                  question["answer"], 
                                                 ))
                        question["tests"].each do |q|
                            io.write(lox_testcase(q.keys()[0],
                                                  q.values()[0]))
                        end
                        io.write(lox_question_bottom());
                    end
                in "scanner"
                    File.open("#{build_dir}/#{week}_questions.xml", "a+") do |io| 
                        io.write(scanner_question_top(question["title"],
                                                      question["question"], 
                                                      question["answer_template"],
                                                      question["answer"], 
                                                     ))
                        question["tests"].each do |q|
                            io.write(scanner_question_testcase(q.keys()[0],
                                                               q.values()[0]))
                        end
                        io.write(scanner_question_bottom());
                    end
                in "essay"
                    File.open("#{build_dir}/#{week}_questions.xml", "a+") do |io| 
                        io.write(essay_question(question["title"],
                                                question["question"], 
                                                question["answer"]
                                               ))
                    end
                end
            end
    end
    File.open("#{build_dir}/#{week}_questions.xml", "a+") {|io| io.write("</quiz>")}
end