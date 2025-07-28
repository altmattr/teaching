require_relative 'templates.rb'

build_dir = "../build"
Dir.glob("../week*/*.md") do |filename| 
    lo = nil
    venue = nil
    question = nil
    puts filename
    week = filename[/\.\.\/(.*)\/.*\.md/,1]
    output = "gift"
    puts week
    # new week means make all the files
    File.open("#{build_dir}/#{week}_glossary.xml", "w") {|io| io.write(glossary_header(week))}
    File.open("#{build_dir}/#{week}.gift", "w") {|io| io.write("")}
    File.open("#{build_dir}/#{week}.yaml", "w") {|io| io.write("")}

    File.readlines(filename, comp: true).each do |line|
      catch (:break) do
        if question && (line =~ /^#.*/) then                 # we've hit a new heading
            File.open("#{build_dir}/#{week}.gift", "a+") {|io| io.write("\n\n")}
            File.open("#{build_dir}/#{week}.yaml", "a+") {|io| io.write("\n\n")}
            question = nil
        end
        /^\*\*(.*)\*\*\:(.*)$/.match(line) do |m|            # glossary item
            File.open("#{build_dir}/#{week}_glossary.xml", "a+") {|io| io.write(glossary_entry(m[1],m[2]))}
        end
        /^#\s+(.*)$/.match(line) do |m|                      # heading 1 for learning outcome
            lo = m[1].downcase.strip.gsub(/\s/, '_')
            puts lo
            throw :break
        end
        /^##\s+(.*)$/.match(line) do |m|                     # heading 2 for venue
            venue = m[1].downcase.strip.gsub(/\s/, '_')
            File.open("#{build_dir}/#{week}.gift", "a+") do |io| 
                # io.write("$CATEGORY: week_#{week}/#{lo}/#{venue}\n\n") # doing an experiment where I remove lo from question bank
                io.write("$CATEGORY: #{week}/#{venue}\n\n") # doing an experiment where I remove lo from question bank
            end
            File.open("#{build_dir}/#{week}.yaml", "a+") do |io| 
                # io.write("---\ncategory:\n  $course$/week_#{week}/#{lo}/#{venue}\n\n")
                io.write("---\ncategory:\n  $course$/#{week}/#{venue}\n\n") # doing an experiment where I remove lo from question bank
            end
            puts "  #{venue}"
            throw :break
        end
        /^###\s+(.*)html$/.match(line) do |m|                # heading 3 for question but html
            output = "gift"
            question = m[1].downcase.strip.gsub(/\s/, '_')
            File.open("#{build_dir}/#{week}.gift", "a+") do |io| 
                io.write("::#{question}::\n[html]")
            end
            puts "    #{question}"
            throw :break
        end
        /^###\s+(.*)<(.*)>$/.match(line) do |m|                # heading 3 for question but going to xml
            output = "yaml"
            question = m[1].downcase.strip.gsub(/\s/, '_')
            File.open("#{build_dir}/#{week}.yaml", "a+") do |io| 
                io.write("\n---\ntitle:\n  #{question}\ntype:\n  #{m[2]}\n")
            end
            puts "    #{question}"
            throw :break
        end
        /^###\s+(.*)$/.match(line) do |m|                    # heading 3 for question (just gift)
            output = "gift"
            question = m[1].downcase.strip.gsub(/\s/, '_')
            File.open("#{build_dir}/#{week}.gift", "a+") do |io| 
                io.write("::#{question}::\n[markdown]")
            end
            puts "    #{question}"
            throw :break
        end
        if question && (line !~ /^#.*/)then                  # just some text to dump into the gift file because it is the gift file text
            File.open("#{build_dir}/#{week}.#{output}", "a+") do |io| 
                io.write(line)
            end
        end
      end
    end
    # week done close glossary
    File.open("#{build_dir}/#{week}_glossary.xml", "a+") {|io| io.write(glossary_footer())}
end

