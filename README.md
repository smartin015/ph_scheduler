
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dateutil

TODO

- [ ] test download and schedule flow with real calendar
- [ ] uploader.py

v2

- [ ] better scheduling
	- are all classes the same length? If not, add to metadata and apply bin-packing
	- take into account "to_schedule" count so that it's not all one class
	- sanity check class times (e.g. don't start before 7am or after 10pm?)
	- if there are too many classes, how to prioritize? 
	- if there are too few classes / spare times, how to decide which times are best?