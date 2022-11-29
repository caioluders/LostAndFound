# Lost & Found
```
    :･ﾟ✧:･ﾟ✧:☆*:✧:･ﾟ✧::☆*:･ﾟ✧::☆*::･ﾟ:☆*:ﾟ✧:･ﾟ:☆*::･ﾟ:☆*::･ﾟ✧
    (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧:::::𝓛𝓸𝓼𝓽 & 𝓕𝓸𝓾𝓷𝓭:::::。.:☆*:･'(*⌒―⌒*)))
    :･ﾟ✧:･ﾟ✧:☆*:✧:･ﾟ✧::☆*:･ﾟ✧::☆*::･ﾟ:☆*:ﾟ✧:･ﾟ:☆*::･ﾟ:☆*::･ﾟ✧
```

The tool helps you find broken, wrong and expired assets on any application. 

## Usage

```
usage: LostAndFound.py - [-h] - [-u URL | -a APK | -d DIR | -i IPA | -b BIN | -t TXT | -p PROXY]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to check
  -a APK, --apk APK     APK to check
  -d DIR, --dir DIR     Directory of Source Code to check
  -i IPA, --ipa IPA     IPA to check
  -b BIN, --bin BIN     Binary to check
  -t TXT, --txt TXT     Text file to check
  -p PROXY, --proxy PROXY
                        Proxy to check
```

First input the desired application to check, the tool will then extract every URL it finds and pass it to the respective checkers. The checker will look if the URL has a broken asset, a expired domain, etc.

```
$ python3 LostAndFound.py -u http://aratu.boitatech.com.br/

    :･ﾟ✧:･ﾟ✧:☆*:✧:･ﾟ✧::☆*:･ﾟ✧::☆*::･ﾟ:☆*:ﾟ✧:･ﾟ:☆*::･ﾟ:☆*::･ﾟ✧
    (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧     𝓛𝓸𝓼𝓽 & 𝓕𝓸𝓾𝓷𝓭         。.:☆*:･'(*⌒―⌒*)))
    :･ﾟ✧:･ﾟ✧:☆*:✧:･ﾟ✧::☆*:･ﾟ✧::☆*::･ﾟ:☆*:ﾟ✧:･ﾟ:☆*::･ﾟ:☆*::･ﾟ✧
	
URL:  http://aratu.boitatech.com.br/
- ['https://aratu.boitatech.com.br', 'https://aratu.boitatech.com.br/images-event/meta-image.png', 'https://aratu.boitatech.com.br', 'https://aratu.boitatech.com.br/images-event/meta-image.png', 'https://platform-api.sharethis.com/js/sharethis.js#property=6254e99180366d0019fc1adf&product=sticky-share-buttons', 'https://forms.gle/oLHmm4V6HzZxr2Pr6', 'https://discord.gg/7xrXqR8x5T', 'https://ctf-api.boitatech.com.br/login', 'https://www.hakaioffensivesecurity.com/', 'https://crowsec.com.br/', 'https://hackingclub.com/', 'https://www.bughunt.com.br/', 'https://www.convisoappsec.com/', 'https://idwall.co/', 'https://www.faculdadevincit.edu.br/cursos', 'https://discord.gg/7xrXqR8x5T', 'https://twitter.com/boitatech', 'https://instagram.com/boitatech', 'https://github.com/boitatech', 'https://www.googletagmanager.com/gtag/js?id=G-SJF22ZP7FR']
100%|█████████████████████████████████████████████████████████████████████████████████| 14/14 - [00:01<00:00, 13.61it/s]
```

## Checkers

They check (duh) if this asset is broken.

- [ ] npm
- [X] twitter
- [X] github
- [ ] TikTok
- [ ] instagram
- [ ] Youtube
- [X] domain
- [X] bitbucket
- [X] gitlab
- [ ] rubygems
- [ ] pypi
- [ ] packagist/composer
- [X] S3
- [ ] buckets

## Extractors

Given an input, they extract (duh again) all the URLS they find and pass them to the respective checkers.

- [X] apk
- [ ] ipa
- [X] website
- [X] binary
- [X] Burp Plugin
- [X] source code


## Burp Plugin
The tool also can be used inside Burp Suite. Load `burp_plugin/LostAndFound_burp_plugin.py` using Jython. The plugin is fully passive and will only check the passing requests.
