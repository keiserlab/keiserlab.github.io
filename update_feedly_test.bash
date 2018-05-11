#/bin/bash
source /srv/home/ecaceres/.bash_profile
admin_email='ecaceres@keiserlab.org';
run_py=$JBDISTRIBUTOR"/jbdistributor/jbdistributor.py";
peeps=$JBDISTRIBUTOR"/data/peeps.tsv";
jname="journalblitz";
users_per_article="2";
last_update_file=$JBARCHIVE_LOC"/last_update.pkl";
log_file=$JBARCHIVE_LOC"/log.tsv";
archive=$JBARCHIVE_LOC"/archive";


# Call jbdistributor
# has last update, has log, archives

echo "current directory: " 
pwd 
echo "shell: "
echo $SHELL 
source /srv/home/ecaceres/anaconda2/envs/py3env/bin/activate /srv/home/ecaceres/anaconda2/envs/py3env
python $run_py $peeps $jname $users_per_article -p $last_update_file -l $log_file -a $archive ; 

git add *

git commit -a -m "Feedly auto-commit: $(date)"

git push --all origin

source deactivate
