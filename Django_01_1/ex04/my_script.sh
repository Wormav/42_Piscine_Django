# Create virtual env "django_venv"
python3 -m venv django_venv

# Activate the env
source django_venv/bin/activate

# Installe pip and lib in requirement.txt
pip install --upgrade pip
pip install -r requirement.txt

# Active venv after run this script
exec bash --rcfile <(echo "source $VENE_DIR/bin/activate")