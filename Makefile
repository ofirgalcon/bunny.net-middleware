include /usr/local/share/luggage/luggage.make
TITLE=BunnynetMiddleware
REVERSE_DOMAIN=com.github.ofirgalcon.bunnynetmiddleware
PACKAGE_VERSION=1.0
PAYLOAD=pack-middleware \
        pack-script-postinstall

pack-middleware:
		@sudo mkdir -p ${WORK_D}/usr/local/munki
		@sudo ${CP} ./middleware_bunny.py ${WORK_D}/usr/local/munki
		@sudo chown root:wheel ${WORK_D}/usr/local/munki/middleware_bunny.py
		@sudo chmod 600 ${WORK_D}/usr/local/munki/middleware_bunny.py
		@sudo chown root:wheel ${WORK_D}/usr/local/munki/munkiaccess.pem
		@sudo chmod 400 ${WORK_D}/usr/local/munki/munkiaccess.pem
