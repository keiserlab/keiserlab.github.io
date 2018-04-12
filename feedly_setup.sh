#/bin/sh

admin_email='ecaceres@keiserlab.org';
run_py=$JBDISTRIBUTOR"/jbdistributor/jbdistributor.py";
peeps=$JBDISTRIBUTOR"/data/peeps.tsv";
jname="journalblitz";
users_per_article="3";
last_update_file=$JBARCHIVE_LOC"/last_update.pkl";
log_file=$JBARCHIVE_LOC"/log.tsv";
archive=$JBARCHIVE_LOC"/archive";

# Call jbdistributor
# has last update, has log, archives
source activate py3env
python $run_py $peeps $jname $users_per_article -p $last_update_file -l $log_file -a $archive -o days=-1 -s weeks=-1; 

# Finally, update the github
git add *

git commit -a -m "Feedly auto-commit: $(date)"

git push --all origin
source deactivate
