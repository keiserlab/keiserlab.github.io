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
python $run_py $peeps $jname $users_per_article -p $last_update_file -l $log_file -a $archive ; 

if [[ $? != 0 ]] then
   mail -s "Feedly XML run failed" $admin_email
   exit 1
fi

# Finally, update the github
git add *
if [[ $? != 0 ]] then 
   mail -s "Feedly add failed" $admin_email
   exit 1
fi

git commit -a -m "Feedly auto-commit: $(date)"
if [[ $? != 0 ]] then 
   mail -s "Feedly commit failed" $admin_email
   exit 1
fi

git push --all origin
if [[ $? != 0 ]] then 
   mail -s "Feedly push failed" $admin_email
   exit 1
fi

mail -s "Feedly push ok" $admin_email

