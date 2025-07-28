require_relative 'templates.rb'
require 'yaml'
require 'pandoc-ruby'

build_dir = "../build"
Dir.glob("#{build_dir}/*.yaml") do |filename| 
    puts filename
    week = filename[/\.\.\/build\/(.*)\.yaml/,1]
    output = "xml"
    puts week
    category = ""
    categories = []
    questions = YAML.load_stream(File.read(filename))
    questions.each do |question|
            if question.key?("category") then
                category = question["category"][/^.*\/(.*)$/,1]
                puts category
                if !categories.include?(category) then
                    categories << category
                    title = case category
                              when "sse" then "Self Study Exercises"
                              when "rat" then "Rapid Application Test"
                              when "fat" then "Application Exercise"
                              else "Questions" 
                            end
                    File.open("#{build_dir}/#{week}_#{category}.tex", "w") do |io| io.write("
                        \\documentclass[twoside=false, DIV=14]{scrartcl}
                        \\input{../latex_setup.tex}
                        \\title{\\color{redish} \\vspace{-1em}COMP3000 Week 6: #{title}}
                        \\begin{document}
                        {\\color{blackish}\\maketitle}
                        ")
                    end
                end
            else
                puts "  #{question["title"]}"
                case question["type"]
                # these question types are not going into latex
                in "lox"
                    # File.open("#{build_dir}/#{week}_questions.latex", "a+") do |io| 
                    #     io.write(lox_question_top(question["title"],
                    #                               question["question"], 
                    #                               question["answer"], 
                    #                              ))
                    #     question["tests"].each do |q|
                    #         io.write(lox_testcase(q.keys()[0],
                    #                               q.values()[0]))
                    #     end
                    #     io.write(lox_question_bottom());
                    # end
                in "scanner"
                    # File.open("#{build_dir}/#{week}_questions.latex", "a+") do |io| 
                    #     io.write(scanner_question_top(question["title"],
                    #                                   question["question"], 
                    #                                   question["answer_template"],
                    #                                   question["answer"], 
                    #                                  ))
                    #     question["tests"].each do |q|
                    #         io.write(scanner_question_testcase(q.keys()[0],
                    #                                            q.values()[0]))
                    #     end
                    #     io.write(scanner_question_bottom());
                    # end
                in "essay"
                    File.open("#{build_dir}/#{week}_#{category}.tex", "a+") do |io| 
                        quest = question["question"]
                        quest = quest.gsub(/<img src=\"(.*)\"\/>/) do |match|
                                          "\n\\includegraphics[width=\\textwidth]{../#{week}/#{$1}}\n"
                                end
                        answer = question["answer"]
                        answer = answer.gsub(/<img src=\"(.*)\"\/>/) do |match|
                                          "\n\\includegraphics[width=\\textwidth]{../#{week}/#{$1}}\n"
                                end

                        io.write(essay_question_latex(question["title"].gsub("_"," "),
                                                      PandocRuby.convert(quest, from: :markdown, to: :latex), 
                                                      PandocRuby.convert(answer, from: :markdown, to: :latex)
                                                     ))
                    end
                end
            end
    end
    combiner = "pdfunite "
    categories.each do |cat|
      File.open("#{build_dir}/#{week}_#{cat}.tex", "a+") {|io| io.write("\\end{document}")}
      puts `pdflatex -output-directory=#{build_dir} #{build_dir}/#{week}_#{cat}.tex`
      combiner += "#{build_dir}/#{week}_#{cat}.pdf "
    end
    combiner += "#{build_dir}/#{week}_all.pdf"
    puts `#{combiner}`
end