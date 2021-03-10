const fs = require("fs")
const https = require("https")
  
try {
  fs.accessSync("./words.md", fs.constants.F_OK)
} catch (err) {
  console.log("couldn't find words.md in current directory, please make that happen! run kindle-to-md.py :)")
  process.exit()
}

const words = fs.readFileSync("./words.md").toString().split("\n").filter(e => e.length)
const word = words[parseInt(Math.random() * words.length - 1)]

console.log("looking up", word)
// use https://dictionaryapi.dev/
const opts = {
  hostname: 'api.dictionaryapi.dev',
  port: 443,
  path: encodeURI(`/api/v2/entries/en_US/${word}`)
}
const req = https.get(opts, res => {
  console.log("waiting")
  res.on("data", d => {
    console.log(JSON.stringify(JSON.parse(d), null, 2))
  })
})

req.on("error", console.log)
