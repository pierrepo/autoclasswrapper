# How to release


## Setup

Install required packages:
```
$ pipenv install --dev twine bumpversion
```


## Tests

Before any release, double-check all tests had run successfully:
```
$ make test-coverage
```


## Update version number

We use the tool [bumpversion](https://github.com/peritus/bumpversion) to update and synchronize the version number
across different files:
```
$ pipenv run bumpversion --verbose --config-file devtools/bumpversion.cfg patch
$ git push origin
$ git push origin --tags
```


## Publish in PyPI

Build the package:
```
$ make compile
```

Then upload the package to PyPI:
```
$ make upload-to-pypi
```

Enter your password upon request.


### Add new release on GitHub

On [GitHub release page](https://github.com/pierrepo/autoclasswrapper/releases) :

- Click the *Draft a release* button.
- Select the latest version as *tag version*.
- Add release version as *Release title* (e.g.: v1.3.7).
- Copy and paste the content of the `CHANGELOG.md` in the *Describe this release* field.
- Hit the *Publish Release* button.
