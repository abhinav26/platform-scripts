echo "cleanup Firefox"
rm -rf "/Users/abhinav/Library/Application Support/Firefox/Profiles/cv3v4zkh.default-1377504414332/*"
cp -r Users/abhinav/abhinav/server/temp/cv3v4zkh.default-1377504414332 "/Users/abhinav/Library/Application Support/Firefox/Profiles/"
echo "cleanup Safari"
rm -rf /Users/abhinav/Library/Safari/*
cp -r /Users/abhinav/abhinav/server/temp/Safari /Users/abhinav/Library/
cp -r /Users/abhinav/abhinav/server/temp/com.apple.Safari.plist /Users/abhinav/Library/Preferences/
echo "cleanup Chrome"
rm -rf "/Users/abhinav/Library/Application Support/Google/Chrome/Default/*"
cp -r "/Users/abhinav/abhinav/server/temp/Default" "/Users/abhinav/Library/Application Support/Google/Chrome/"