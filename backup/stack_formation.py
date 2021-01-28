import boto3
import paramiko 
import time
import os 

def ssh_connect_with_retry(ssh, instanceId,instanceDNS, retries):
    if retries > 5:
        return False

    privkey = paramiko.RSAKey.from_private_key_file('./KeyPairProject.pem')
    interval = 10
    try:
        retries += 1
        print("Connexion SSH vers l'instance : {}".format(instanceId))
        ssh.connect(hostname=instanceDNS,
                    username='ubuntu', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print("Retentative SSH vers l'instance {}".format(instanceId))
        instances = ec2.describe_instances(InstanceIds = ids, DryRun = False)
        instances = instances['Reservations']
        ssh_connect_with_retry(ssh, instance['InstanceId'],instance['PublicDnsName'], retries)


ec2 = boto3.client('ec2',region_name='eu-west-3')

instances = ec2.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': 8,
                'VolumeType': 'gp2',
                'Encrypted': True
            }
        },
    ],
    ImageId='ami-089d839e690b09b28',
    InstanceType='t3.medium',
    KeyName='KeyPairProject',
    SecurityGroupIds=['sg-05a1fb5f4033a255d'],
    MinCount=1,
    MaxCount=3)

try:
  
    ids = []

    for instance in instances['Instances']:
        print('Instance {id} est démarrée.'.format(id = instance['InstanceId']))
        ids = ids + [instance['InstanceId']]

    print("On attend un petit moment jusqu'a ce que nos instances soient initialisées et bien configurées.")

    time.sleep(10)

    instances = ec2.describe_instances(InstanceIds = ids, DryRun = False)
    instances = instances['Reservations']

    Name = str()
    for instance in instances[0]['Instances']:
        print('Instance {id} est démarrée. Son dns public est {dns}'.format(id = instance['InstanceId'], dns=instance['PublicDnsName']))
        Name = Name + instance['InstanceId']

    config_data = {}

    print("La configuration de l'environnement d'éxécution va se lancer dans notre cluster de VM.")
    
    path = os.getcwd() + "/log_" + Name
    access_rights = 0o777

    try:
        os.mkdir(path, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    j = 0
    cmd_join = str()

    for instance in instances[0]['Instances']:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        b = ssh_connect_with_retry(ssh, instance['InstanceId'], instance['PublicDnsName'], 0)
        if (b == True):
            print("La connexion SSH a réussi. On commence l'installation de Docker et Kubernetes dans l'instance {}.".format(instance['InstanceId']))
            i = 1
            fo = open("log_" + Name + "/" + instance['InstanceId']+".txt","wb")
            stdin, stdout, stderr = ssh.exec_command("sudo apt-get update && sudo apt-get install -y apt-transport-https curl")
            fo.write('\n La Commande : sudo apt-get update && sudo apt-get install -y apt-transport-https curl \n.'.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
            fo.write('\n La Commande : curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  \n.'.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable"')
            fo.write('\n La Commande : sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable"  \n.'.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')
            fo.write('\n La Commande : curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -   \n.'.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('cat << EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list\ndeb https://apt.kubernetes.io/ kubernetes-xenial main\nEOF\n')
            fo.write('\n La Commande : cat << EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list\ndeb https://apt.kubernetes.io/ kubernetes-xenial main\nEOF\n'.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo apt-get update')
            fo.write('\n La Commande : sudo apt-get update '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo apt-get install -y docker-ce kubelet kubeadm kubectl vim')
            fo.write('\n La Commande : sudo apt-get install -y docker-ce kubelet kubeadm kubectl vim '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee -a /etc/sysctl.conf')
            fo.write('\n La Commande : echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee -a /etc/sysctl.conf '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo sysctl -p')
            fo.write('\n La Commande : sudo sysctl -p  '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo swapoff –a')
            fo.write('\n La Commande : sudo swapoff –a  '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo apt-get install -y openjdk-8-jdk scala git')
            fo.write('\n La Commande : sudo apt install default-jdk scala git -y ' .encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('wget http://sd-127206.dedibox.fr/hagimont/software/hadoop-2.7.1.tar.gz && wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz')
            fo.write('\n La Commande : wget http://sd-127206.dedibox.fr/hagimont/software/hadoop-2.7.1.tar.gz && wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz  '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('tar -xvzf hadoop-2.7.1.tar.gz && tar -xvzf spark-2.4.3-bin-hadoop2.7.tgz && rm hadoop-2.7.1.tar.gz && rm spark-2.4.3-bin-hadoop2.7.tgz')
            fo.write('\n La Commande : tar -xvzf hadoop-2.7.1.tar.gz && tar -xvzf spark-2.4.3-bin-hadoop2.7.tgz  '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('sudo mv hadoop-2.7.1/ /usr/local/ && sudo mv spark-2.4.3-bin-hadoop2.7/ /usr/local/')
            fo.write('\n La Commande : mv hadoop-2.7.1/ /usr/local/ && mv spark-2.4.3-bin-hadoop2.7/ /usr/local/  '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('echo "export HADOOP_HOME=/usr/local/hadoop-2.7.1" >> ~/.profile && source ~/.profile')
            fo.write('\n echo "export HADOOP_HOME=/usr/local/hadoop-2.7.1" >> ~/.profile '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command("echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.profile && source ~/.profile")
            fo.write('\n echo "export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin" >> ~/.profile && source ~/.profile '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('echo "export SPARK_HOME=/usr/local/spark-2.4.3-bin-hadoop2.7" >> ~/.profile && source ~/.profile')
            fo.write('\n echo "export SPARK_HOME=/usr/local/spark-2.4.3-bin-hadoop2.7" >> ~/.profile && source ~/.profile '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command("echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.profile && source ~/.profile")
            fo.write('\n echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.profile && source ~/.profile '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            stdin, stdout, stderr = ssh.exec_command('echo "JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >> ~/.profile && source ~/.profile')
            fo.write('\n echo "JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >> ~/.profile && source ~/.profile '.encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))
            if (j == 0):
                stdin, stdout, stderr = ssh.exec_command('sudo hostnamectl set-hostname master-node')
                fo.write('\n La Commande : sudo hostnamectl set-hostname master-node  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('sudo kubeadm init --pod-network-cidr=10.244.0.0/16')
                cpt = 0
                stdout_str = str()
                for line in ((stdout.read()).decode('utf-8')).split('\n'):
                    stdout_str = stdout_str + line + '\n'
                    if ((line[0:12] == 'kubeadm join') or (cpt==1)):
                        cmd_join = cmd_join + line + '\n'
                        cpt=+1
                        if (cpt == 2):
                            break
                    else: 
                        continue
                fo.write('\n La Commande : sudo kubeadm init --pod-network-cidr=10.244.0.0/16  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout_str.encode())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('mkdir -p $HOME/.kube')
                fo.write('\n La Commande : mkdir -p $HOME/.kube  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config')
                fo.write('\n La Commande : sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('sudo chown $(id -u):$(id -g) $HOME/.kube/config')
                fo.write('\n La Commande : sudo chown $(id -u):$(id -g) $HOME/.kube/config  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml')
                fo.write('\n La Commande : sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                j=j+1
            else:
                stdin, stdout, stderr = ssh.exec_command('sudo hostnamectl set-hostname worker{}'.format(j))
                fo.write(('\n sudo hostnamectl set-hostname worker{} '.format(j)).encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml')
                fo.write('\n La Commande : sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml  '.encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('sudo ' + cmd_join)
                fo.write(('\n' + 'La Commande : sudo ' + cmd_join).encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                stdin, stdout, stderr = ssh.exec_command('cd /usr/local/spark-2.4.3-bin-hadoop2.7 && sudo bin/docker-image-tool.sh -r spark -t latest ./usr/local/spark-2.4.3-bin-hadoop2.7/kubernetes/dockerfiles/spark/Dockerfile build && sudo docker image ls')
                fo.write(('\n' + 'cd /usr/local/spark-2.4.3-bin-hadoop2.7 && sudo bin/docker-image-tool.sh -r spark -t latest ./usr/local/spark-2.4.3-bin-hadoop2.7/kubernetes/dockerfiles/spark/Dockerfile build && sudo docker image ls ').encode())
                fo.write('stdout : '.encode())
                fo.write(stdout.read())
                fo.write('stderr : '.encode())
                fo.write(stderr.read())
                i = i + 1
                print('step {}'.format(i))
                j=j+1
            stdin, stdout, stderr = ssh.exec_command('java -version; javac -version; scala -version; git --version; spark-submit --version')
            fo.write('\n La Commande : java -version; javac -version; scala -version; git --version; spark-submit --version ' .encode())
            fo.write('stdout : '.encode())
            fo.write(stdout.read())
            fo.write('stderr : '.encode())
            fo.write(stderr.read())
            i = i + 1
            print('step {}'.format(i))           
            ssh.close()
        else:
            print("Connexion SSH vers l'instance {} n'a pas réussi".format(instance['InstanceId']))

    #instance = instances[0]['Instances'][0]
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #b = ssh_connect_with_retry(ssh, instance['InstanceId'], instance['PublicDnsName'], 0)    
    #if (b == True):
        #print("We are good {}".format(instance['InstanceId']))
        #ftp_client=ssh.open_sftp()
        #ftp_client.put('./word_count.py','/home/ubuntu/')
        #ftp_client.close()
        #i = i + 1
        #print('step {}'.format(i))
    #else:
        #print("We are not")
except Exception as e:
    print(e)
    ec2.terminate_instances(InstanceIds = ids, DryRun = False)
    print("Tout les instances ont été résiliées à cause d'une erreur")
    
