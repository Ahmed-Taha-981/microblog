# SonarQube Local Server Setup Guide (WSL/Linux)

## Prerequisites
- ✅ Java 17 (you have OpenJDK 17.0.17)
- WSL/Linux environment

## Step-by-Step Installation

### 1. Download SonarQube Community Edition

```bash
cd ~
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-10.6.1.86982.zip
```

Or download manually from: https://www.sonarsource.com/products/sonarqube/downloads/

### 2. Extract SonarQube

```bash
unzip sonarqube-10.6.1.86982.zip
mv sonarqube-10.6.1.86982 sonarqube
cd sonarqube
```

### 3. Configure SonarQube (Optional - for memory optimization)

Edit `conf/sonar.properties` if needed:
```bash
nano conf/sonar.properties
```

You can adjust memory settings if you have limited RAM (default is usually fine).

### 4. Start SonarQube

For Linux/WSL:
```bash
./bin/linux-x86-64/sonar.sh start
```

Or to run in foreground (to see logs):
```bash
./bin/linux-x86-64/sonar.sh console
```

### 5. Check Status

```bash
./bin/linux-x86-64/sonar.sh status
```

### 6. View Logs

```bash
tail -f logs/sonar.log
```

### 7. Access SonarQube

Open your browser and go to: **http://localhost:9000**

Default credentials:
- Username: `admin`
- Password: `admin` (you'll be prompted to change it on first login)

---

## Quick Start Commands (All in One)

```bash
# Navigate to home directory
cd ~

# Download SonarQube (if not already downloaded)
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-10.6.1.86982.zip

# Extract
unzip sonarqube-10.6.1.86982.zip
mv sonarqube-10.6.1.86982 sonarqube

# Navigate to SonarQube directory
cd sonarqube

# Start SonarQube
./bin/linux-x86-64/sonar.sh start

# Wait a minute, then check status
./bin/linux-x86-64/sonar.sh status

# View logs to see when it's ready
tail -f logs/sonar.log
```

Press `Ctrl+C` to exit log viewing.

---

## Managing SonarQube

### Start SonarQube
```bash
cd ~/sonarqube
./bin/linux-x86-64/sonar.sh start
```

### Stop SonarQube
```bash
cd ~/sonarqube
./bin/linux-x86-64/sonar.sh stop
```

### Restart SonarQube
```bash
cd ~/sonarqube
./bin/linux-x86-64/sonar.sh restart
```

### Check Status
```bash
cd ~/sonarqube
./bin/linux-x86-64/sonar.sh status
```

---

## Analyzing Your Microblog Project

### 1. Download SonarScanner

```bash
cd ~
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
mv sonar-scanner-5.0.1.3006-linux sonar-scanner
```

### 2. Add SonarScanner to PATH (add to ~/.bashrc)

```bash
echo 'export PATH=$PATH:~/sonar-scanner/bin' >> ~/.bashrc
source ~/.bashrc
```

### 3. Navigate to Your Project

```bash
cd /mnt/c/Users/Ahmed/Desktop/microblog
```

### 4. Generate a Token in SonarQube

1. Go to http://localhost:9000
2. Login with admin/admin
3. Go to: **My Account** → **Security** → **Generate Token**
4. Copy the token

### 5. Run Analysis

```bash
sonar-scanner \
  -Dsonar.projectKey=microblog \
  -Dsonar.sources=app \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN_HERE
```

Or use the `sonar-project.properties` file:
```bash
sonar-scanner -Dsonar.login=YOUR_TOKEN_HERE
```

---

## Troubleshooting

### Port 9000 Already in Use
```bash
# Find what's using port 9000
sudo netstat -tulpn | grep 9000
# Or
sudo lsof -i :9000
```

### Java Not Found
```bash
# Verify Java is in PATH
which java
java -version

# If not found, add to PATH
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
```

### Permission Denied
```bash
# Make scripts executable
chmod +x ~/sonarqube/bin/linux-x86-64/sonar.sh
chmod +x ~/sonar-scanner/bin/sonar-scanner
```

### Memory Issues
SonarQube requires at least 2GB RAM. If you have limited memory, edit `conf/sonar.properties`:
```bash
nano ~/sonarqube/conf/sonar.properties
```

Look for `sonar.web.javaOpts` and reduce memory if needed.

### Cannot Access from Windows Browser
If `localhost:9000` doesn't work from Windows, try:
- `http://127.0.0.1:9000`
- Or find your WSL IP: `ip addr show eth0` and use that IP

---

## Useful Commands Summary

```bash
# Start SonarQube
~/sonarqube/bin/linux-x86-64/sonar.sh start

# Stop SonarQube
~/sonarqube/bin/linux-x86-64/sonar.sh stop

# Check status
~/sonarqube/bin/linux-x86-64/sonar.sh status

# View logs
tail -f ~/sonarqube/logs/sonar.log

# Run analysis on your project
cd /mnt/c/Users/Ahmed/Desktop/microblog
sonar-scanner -Dsonar.login=YOUR_TOKEN
```
