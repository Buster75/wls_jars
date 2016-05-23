#!/produkter/gnu/python/bin/python2
# -*- coding: iso-8859-15 -*-
'''
Created on 11 apr 2016
@author: Thomas Bergqvist
'''
import os, sys
class Jars():
    def __init__(self, domain, user):
        self.domain = domain
        self.user = user
        self.sokvag = "/domains/" + user +"/" + domain + "/applications"

    def check(self):
        print("Kollar brustna länkar under applications...")
        nrofbrokenlink = 0
        try:
            filer = os.listdir(self.sokvag)
        except:
            print("Något gick snett, avslutar!")
            exit()
        for i in filer:
            tmppath = self.sokvag +"/" + i
            if os.path.islink(tmppath):
                if os.path.exists(tmppath):
                    pass
                else:
                    print(tmppath +" Är en brusten länk...")
                    print("")
                    nrofbrokenlink += 1
        if nrofbrokenlink == 0:
            print("Här fanns inga brustna länkar...")

        print("".ljust(60,'-'))
        print("Kollar classpath...")

        appserver_env_file = "/domains/" + self.user +"/" + self.domain +"/settings/appserver1.env"
        appserver_str =""
        if  os.path.exists(appserver_env_file):
            try:
                appserverfile = open(appserver_env_file, "r")
                appserver_str = appserverfile.read()
                appserverfile.close()
            except IOError:
                print("Kunde inte öppna appserver_env ")
                print("Avslutar!")
                exit()
        else:
            print("Hittar inte " + appserver_env_file)
            print("Avslutar!")
            exit()

        appserver1_classpath_env_file = "/domains/" + self.user +"/" + self.domain +"/weblogic-root/appserver1_classpath.env"
        if  os.path.exists(appserver1_classpath_env_file):
            try:
                appserverfile2 = open(appserver1_classpath_env_file, "r")
                appserver_str2 = appserverfile2.read()
                appserverfile2.close()
                appserver_str = appserver_str + appserver_str2
            except IOError:
                print("Kunde inte öppna appserver1_classpath.env ")
                print("Fortsätter...")
        else:
            print("Hittar inte " + appserver1_classpath_env_file)
            print("Fortsätter...")

        jarstochech, linkstocheck  = [],[]
        for dirpath, dirnames, filenames in os.walk(self.sokvag,followlinks=True):
            for fname in filenames:
                if fname.endswith("jar"):
                    if os.path.islink(os.path.join(dirpath, fname)):
                        linkstocheck.append(os.path.join(dirpath, fname))
                    else:
                        jarstochech.append(os.path.join(dirpath, fname))

        for j in linkstocheck:
            realfilenamestartindex = os.path.realpath(j).rfind("/")
            realfile = os.path.realpath(j)[realfilenamestartindex + 1:len(os.path.realpath(j))]
            linknamestartindex = j.rfind("/")
            linkname = j[linknamestartindex + 1:len(j)]
            if (linkname and realfile) in appserver_str:
                print(linkname + " Är en länk till, " + realfile)
                print("Du kan ta bort " + realfile)
                print("")
                try:
                    jarstochech.remove(os.path.dirname(j) + "/" + realfile)
                except ValueError:
                    continue
            elif (linkname and realfile) not in appserver_str:
                try:
                    jarstochech.remove(os.path.dirname(j) + "/" + realfile)
                except ValueError:
                    continue
            elif linkname not in appserver_str:
                jarstochech.remove(os.path.dirname(j) + "/" + realfile)
            elif realfile not in appserver_str:
                jarstochech.remove(os.path.dirname(j) + "/" + realfile)
        nrofmissingjars = 0
        print("Saknade jar i classpath:")
        for j in jarstochech:
            start = j.rfind("/")
            filenametocheck = j[start + 1:len(j)]
            if filenametocheck not in appserver_str:
                print(j)
                nrofmissingjars += 1
        if nrofmissingjars == 0:
            print("Inga alls... en enda kunde du väl ha glömt iallafall.")
        print("".ljust(60,'-'))

def main():
    print("")
    user = os.environ['USER']
    if len(sys.argv) != 2:
        print('''Skriptet tar ett argument: [wlsdomännamn] t.ex dmvas.
skriptet kollar brusta länkar under wlsdomännamn/applications
och listar saknade jar filer i appserver.env och i appserver1_classpath.env
om den finns. Skriptet försöker även kolla om man råkat specificera
dubbletter när leveransen innehåller länkar.
''')
        exit()
    else:
        domain = sys.argv[1]
        print("       Domän " + domain)
        print("")
        jars = Jars(domain, user)
        jars.check()
        print("")
        print("       Hej då.")

if __name__ == '__main__':
    main()
