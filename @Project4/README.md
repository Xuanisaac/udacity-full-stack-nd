Udacity Full Stack Project Tournament Results
=============

### Install

To use [Vagrant](http://www.vagrantup.com/downloads.html) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads) and Python, please follow the instructions on their website.

If you have trouble, check out this [wiki entry from the helpful folks @ Udacity](https://www.udacity.com/wiki/ud197/install-vagrant)

### Usage

1. Download or clone this repository to your local machine
2. Use the command `cd /vagrant/tournament` to start Vagrant and change to VM's working directory
    ```
    vagrant up
    
    vagrant ssh
    
    cd vagrant
    ```
3. Use psql to generate SQL DB using `tournament.sql`
  ```
  psql
  
  \i tournament.sql
  
  \q
  ```
5. Run Tests
  ```
  python tournament_test.py
  ```
  
