# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.define "app" do |app|
    app.vm.hostname = "app"

    app.vm.network "private_network", ip: "192.168.56.26"
    app.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true, id: "core-api"
    app.vm.network "forwarded_port", guest: 27017, host: 27017, auto_correct: true, id: "core-db"
    app.vm.network "forwarded_port", guest: 8501, host: 8501, auto_correct: true, id: "core-streamlit"

    app.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "/home/vagrant/ansible/main.yml"
      ansible.inventory_path = "/home/vagrant/ansible/hosts"
      ansible.config_file = "/home/vagrant/ansible/ansible.cfg"
      ansible.galaxy_roles_path = "/home/vagrant/ansible/roles"
      ansible.galaxy_role_file = '/home/vagrant/ansible/requirements.yml'
      ansible.verbose = true
      ansible.become = true
      ansible.become_user = "root"
    end
  end

  config.vm.synced_folder "app/", "/home/vagrant/app", type: "rsync",
      create: true, group: "vagrant", owner: "vagrant",
      id: "app"
  config.vm.synced_folder "database/", "/home/vagrant/database", type: "rsync",
      create: true, group: "vagrant", owner: "vagrant",
      id: "database"
  config.vm.synced_folder "ansible/", "/home/vagrant/ansible", type: "rsync",
      create: true, group: "vagrant", owner: "vagrant",
      id: "ansible"
  config.vm.provision "file", source: "docker-compose.yml", destination: "docker-compose.yml"

  # config.vm.define "db" do |db|
  #   db.vm.network "forwarded_port", guest: 27017, host: 27017, auto_correct: true, id: "core-db"
  # end
  # config.vm.define "streamlit" do |streamlit|
  #   streamlit.vm.network "forwarded_port", guest: 8501, host: 8501, auto_correct: true, id: "core-streamlit"
  # end
end
