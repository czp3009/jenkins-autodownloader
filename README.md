# Jenkins auto-downloader
Automatic download artifacts in all builds from Jenkins.

# Usage
```bash
python downloader.py {branchUrl} {matchExr} {outputDir}
```

`branchUrl`: The url of a branch

`matchExr`: An regular expression used to select which artifact should be download by artifact file name

`outputDir`: Download to this folder

Example:
```bash
python downloader.py https://build.torchapi.net/job/Torch/job/Torch/job/master torch-server.zip Torch
```

# License
Apache 2.0
