require 'base64'

Dir.glob("../build/*.{gift,xml}") do |filename| 
    data = File.read(filename)
    week = filename[/\.\.\/build\/(.*)_.*/,1]

    new_data = data.gsub(/<img src=\"(.*)\"\/>/) do |match|
        "<img src=\"data:image\/png;base64, "+ Base64.encode64(File.open("../#{week}/#{$1}", "rb").read) + "\" \/>"
    end
    new_data = new_data.gsub(/<img src\\=\"(.*)\"\/>/) do |match|
        "<img src\\=\"data:image\/png;base64, "+ Base64.encode64(File.open("../#{week}/#{$1}", "rb").read).gsub(/=/,"\\=") + "\" \/>"
    end
    new_data = new_data.gsub(/<code src=\"(.*)\"\/>/) do |match|
        "<pre>\n"+File.open($1, "rb").read
                                     .gsub(/^ /," &nbsp ")
                                     .gsub(/^\s*$/,"&nbsp")
                                     .gsub(/\{/,"\\{")
                                     .gsub(/\}/,"\\}") + "\n<\/pre>"
    end
    File.write(filename, new_data)
end 