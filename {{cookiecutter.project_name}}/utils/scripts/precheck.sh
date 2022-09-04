#! /bin/bash
#
# Check the machine meets the requirements.
# RUN: source ./utils/scripts/precheck.sh
#

python3 --version >/dev/null 2>&1 && echo "✔ `python3 --version` is installed." || {
    echo >&2 -e "\npython 3.X is required but it's not installed."
    echo >&2 -e "You can download & install it from the following link:\n"
    echo >&2 -e "\nPython download page: https://www.python.org/downloads/"
    exit 1;
}

pip3 --version >/dev/null 2>&1 && echo "✔ Pip is installed." || {
    echo >&2 -e "\npip is required but it's not installed."
    echo >&2 -e "You can install it by running the following command:\n"
    echo >&2 "wget https://bootstrap.pypa.io/get-pip.py --output-document=get-pip.py; chmod +x get-pip.py; sudo -H python3 get-pip.py"
    echo >&2 -e "\n"
    echo >&2 -e "\nFor more information, see pip documentation: https://pip.pypa.io/en/latest/"
    exit 1;
}

node --version >/dev/null 2>&1 && echo "✔ Node `node --version` is installed." || {
    echo >&2 -e "\node is required but it's not installed."
    echo >&2 -e "You can download & install it from the following link:\n"
    echo >&2 -e "\nNode.js download page: https://nodejs.org/en/download/"
    exit 1;
}

npm --version >/dev/null 2>&1 && echo "✔ Npm `npm --version` is installed." || {
    echo >&2 -e "\npm is required but it's not installed."
    echo >&2 -e "\nFor more information: https://www.npmjs.com/package/yarn"
    exit 1;
}

virtualenv --version >/dev/null 2>&1 && echo "✔ Virtualenv is installed." || {
    echo >&2 -e "\nvirtualenv is required but it's not installed."
    echo >&2 -e "You can install it by running the following command:\n"
    echo >&2 "sudo -H pip3 install virtualenv"
    echo >&2 -e "\n"
    echo >&2 -e "\nFor more information, see virtualenv documentation: https://virtualenv.pypa.io/en/latest/"
    exit 1;
}

if [ -z "$VIRTUAL_ENV" ]; then
    echo >&2 -e "\nYou need activate a virtualenv first"
    echo >&2 -e 'If you do not have a virtualenv created, run the following command to create and automatically activate a new virtualenv named "venv" on current folder:\n'
    echo >&2 -e "    $ virtualenv venv --python=\`which python3\`"
    echo >&2 -e "\nTo leave/disable the currently active virtualenv, run the following command:\n"
    echo >&2  "    $ deactivate"
    echo >&2 -e "\nTo activate the virtualenv again, run the following command:\n"
    echo >&2  "    $ source venv/bin/activate"
    echo >&2 -e "\nFor more information, see virtualenv documentation: https://virtualenv.pypa.io/en/latest/"
    echo >&2 -e "\n======================= OR ======================="
    echo >&2 -e "\nTo create & start a virtualenv session via 'pipenv', run:"
    echo >&2 -e "\n    $ pipenv shell"
    echo >&2 -e "\nIf pipenv is not installed, you can install it by running the following command:"
    echo >&2 "\n    $ pip3 install pipenv"
else
    echo "\n"
    echo "🎉 Congratulations!"
    echo "✅ All requirements are satisfied!\n"
    echo "👉🏼 Next step: Follow the local development guide from README.md"
fi
