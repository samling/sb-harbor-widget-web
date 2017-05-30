if [[ $ZSH_EVAL_CONTEXT == "" ]]; then
    echo "Please run with: source env.sh"
else
    export FLASK_APP=main.py
    export FLASK_DEBUG=1
fi
#
