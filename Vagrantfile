$enable_serial_logging = false

Vagrant.configure(2) do |config|
    config.vm.box = "debian/contrib-buster64"

    config.vm.provision "shell", path: "./provision.sh"
    config.vm.synced_folder ".", "/home/vagrant/src"  # <-- exactly as in provision.sh!

    config.vm.provider "virtualbox" do |vb|
        vb.gui = false
        vb.cpus = 2
        vb.memory = 2048
    end
end
