import pymongo
import re
from collections import Counter
import plotly.graph_objects as go


def analysis():
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['jobs']
    collection = db['collection_1']

    # Retrieve all job ads
    job_ads = collection.find()

    # Define categories with their associated keywords
    categories = {
        # .Net ecosystem
        '.Net': ['.net', 'c#', '.net core', 'asp.net', 'vb.net', 'f#'],

        # Python ecosystem
        'Python': ['python', 'django', 'flask', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'keras', 'pytorch',
                   'fastapi', 'scrapy', 'jupyter', 'bokeh', 'matplotlib', 'seaborn'],

        # JavaScript and related frameworks
        'JavaScript': ['javascript', 'react', 'angular', 'vue.js', 'node.js', 'typescript', 'express', 'next.js',
                       'nuxt.js', 'svelte', 'redux', 'gatsby', 'electron', 'meteor', 'jest'],

        # Java ecosystem
        'Java': ['java', 'spring', 'spring boot', 'hibernate', 'junit', 'maven', 'gradle', 'kotlin', 'android',
                 'groovy'],

        # DevOps and Infrastructure as Code
        'DevOps': ['devops', 'docker', 'kubernetes', 'ansible', 'terraform', 'jenkins', 'gitlab ci/cd', 'travis ci',
                   'circleci', 'azure devops', 'prometheus', 'grafana', 'nagios', 'puppet', 'chef', 'vagrant',
                   'spinnaker'],

        # Databases and Data Management
        'Database': ['sql', 'nosql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'cassandra',
                     'couchbase', 'firebase', 'elasticsearch', 'neo4j', 'mariadb', 'redshift', 'snowflake', 'hive',
                     'hbase', 'presto'],

        # Cloud computing platforms and services
        'Cloud': ['aws', 'azure', 'google cloud', 'gcp', 'ibm cloud', 'oracle cloud', 'digitalocean', 'heroku',
                  'firebase', 'cloudflare', 'openstack', 'rackspace'],

        # PHP ecosystem
        'PHP': ['php', 'laravel', 'symfony', 'zend', 'yii', 'cakephp', 'codeigniter', 'drupal', 'wordpress', 'joomla',
                'magento'],

        # Ruby and Rails ecosystem
        'Ruby': ['ruby', 'rails', 'sinatra', 'jruby', 'rvm', 'bundler'],

        # Mobile development
        'Mobile': ['swift', 'kotlin', 'objective-c', 'flutter', 'react native', 'ionic', 'cordova', 'xamarin',
                   'android sdk', 'ios sdk'],

        # Frontend development
        'Frontend': ['html', 'css', 'sass', 'less', 'bootstrap', 'tailwindcss', 'bulma', 'materialize', 'foundation',
                     'jquery', 'typescript', 'webpack', 'gulp', 'grunt', 'babel'],

        # AI/ML and Data Science
        'AI/ML': ['machine learning', 'deep learning', 'artificial intelligence', 'data science', 'tensorflow', 'keras',
                  'pytorch', 'scikit-learn', 'xgboost', 'lightgbm', 'catboost', 'nlp', 'spacy', 'nltk', 'transformers',
                  'opencv', 'dlib', 'yolo', 'huggingface', 'fastai', 'onnx', 'pandas', 'numpy', 'scipy', 'matplotlib',
                  'seaborn', 'plotly', 'jupyter', 'kafka', 'apache spark', 'hadoop', 'airflow', 'mlflow'],

        # Big Data and Distributed Systems
        'Big Data': ['hadoop', 'spark', 'kafka', 'hive', 'hbase', 'flink', 'storm', 'presto', 'mapreduce', 'zookeeper',
                     'sqoop', 'azkaban', 'pig', 'tez', 'druid', 'beam', 'cassandra', 'mongodb', 'couchbase'],

        # Security and Networking
        'Security': ['cybersecurity', 'penetration testing', 'ethical hacking', 'siem', 'splunk', 'wireshark', 'nmap',
                     'burp suite', 'owasp', 'kali linux', 'nessus', 'snort', 'suricata', 'ossec', 'metasploit',
                     'firewall', 'vpn', 'encryption', 'ssl', 'tls', 'identity management', 'iam', 'oauth', 'saml',
                     'sso', 'cissp', 'ceh', 'ccsp', 'cloud security'],

        # Other programming languages and ecosystems
        'Other Languages': ['go', 'scala', 'perl', 'rust', 'elixir', 'erlang', 'haskell', 'r', 'matlab', 'lua', 'vhdl',
                            'verilog', 'assembly', 'cobol', 'fortran', 'pascal', 'ada', 'awk', 'bash',
                            'shell scripting', 'powershell', 'tcl', 'f#', 'racket', 'lisp', 'prolog'],

        # Enterprise and Middleware
        'Enterprise': ['sap', 'oracle', 'salesforce', 'peoplesoft', 'siebel', 'microsoft dynamics', 'ibm websphere',
                       'tibco', 'mulesoft', 'apache camel', 'jboss', 'webmethods', 'soa', 'microservices', 'esb', 'bpm',
                       'workflow', 'api management', 'identity management', 'active directory', 'ldap'],

        # Tools and Utilities
        'Tools': ['git', 'svn', 'mercurial', 'docker', 'kubernetes', 'jenkins', 'ansible', 'chef', 'puppet',
                  'terraform', 'vagrant', 'maven', 'gradle', 'ant', 'gulp', 'grunt', 'webpack', 'babel', 'npm', 'yarn',
                  'pip', 'conda', 'docker-compose', 'helm', 'prometheus', 'grafana', 'nagios', 'splunk', 'logstash',
                  'elasticsearch', 'kibana', 'new relic', 'datadog', 'dynatrace', 'pagerduty', 'jira', 'confluence',
                  'trello', 'slack', 'teams', 'zoom'],

        # Testing and QA
        'Testing': ['selenium', 'cypress', 'junit', 'testng', 'pytest', 'mocha', 'chai', 'jest', 'jasmine', 'karma',
                    'robot framework', 'cucumber', 'postman', 'soapui', 'loadrunner', 'jmeter', 'gatling', 'sonarqube',
                    'pmd', 'checkmarx', 'fortify', 'veracode'],

        # Design and UI/UX
        'Design/UI/UX': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'invision', 'zeplin', 'balsamiq',
                         'marvel', 'axure', 'framer', 'proto.io', 'principle', 'origami studio', 'after effects',
                         'cinema 4d', 'blender', 'unity', 'unreal engine'],

        # IoT and Embedded Systems
        'IoT/Embedded': ['arduino', 'raspberry pi', 'esp32', 'iot', 'mqtt', 'zigbee', 'bluetooth', 'modbus', 'can bus',
                         'rtos', 'freeRTOS', 'vxworks', 'zephyr', 'mbed', 'contiki', 'openwrt', 'firmware', 'fpga',
                         'vhdl', 'verilog', 'embedded c', 'assembly', 'microcontroller', 'pic', 'avr', 'stm32',
                         'ti-rtos', 'lwip', 'openthread', 'mqtt'],

        # Robotics
        'Robotics': ['ros', 'gazebo', 'v-rep', 'robotics', 'control systems', 'path planning', 'slam',
                     'motion planning', 'robot operating system', 'coppelia', 'mujoco', 'differential drive',
                     'quadrupeds', 'robot arm', 'kinematics', 'dynamics', 'robot perception', 'sensor fusion', 'lidar',
                     'camera calibration', 'robotic process automation', 'rpa'],

        # Game Development
        'Game Development': ['unity', 'unreal engine', 'godot', 'cryengine', 'game maker', 'construct', 'cocos2d',
                             'spritekit', 'phaser', 'panda3d', 'jmonkeyengine', 'panda3d', 'three.js', 'blender',
                             'maya', '3ds max', 'zbrush', 'substance painter', 'mudbox', 'houdini'],

        # Blockchain and Cryptocurrency
        'Blockchain': ['blockchain', 'bitcoin', 'ethereum', 'smart contracts', 'solidity', 'hyperledger', 'chaincode',
                       'cryptography', 'web3', 'truffle', 'ganache', 'dapp', 'erc20', 'erc721', 'defi', 'nft',
                       'metamask', 'polkadot', 'cosmos', 'solana', 'avalanche', 'cardano', 'binance smart chain',
                       'ripple', 'stellar'],

        # Data Engineering
        'Data Engineering': ['data engineering', 'etl', 'apache nifi', 'airflow', 'talend', 'informatica', 'ssrs',
                             'ssas', 'ssis', 'apache beam', 'data warehousing', 'snowflake', 'redshift', 'bigquery',
                             'data lake', 'azure data factory', 'databricks', 'hudi', 'iceberg', 'delta lake', 'presto',
                             'trino'],

        # Web Servers and Hosting
        'Web Servers': ['nginx', 'apache', 'iis', 'tomcat', 'jetty', 'glassfish', 'wildfly', 'jboss', 'weblogic',
                        'lamp', 'mean', 'mern', 'wsgi', 'uwsgi', 'gunicorn'],

        # CRM and Marketing Tools
        'CRM/Marketing': ['salesforce', 'hubspot', 'zoho', 'microsoft dynamics', 'pipedrive', 'marketo', 'pardot',
                          'mailchimp', 'constant contact', 'sendgrid', 'drip', 'intercom', 'zendesk', 'sprout social',
                          'hootsuite', 'buffer', 'google analytics', 'facebook ads', 'google ads', 'twitter ads',
                          'linkedin ads', 'semrush', 'ahrefs', 'moz'],

        # E-commerce
        'E-commerce': ['shopify', 'woocommerce', 'magento', 'bigcommerce', 'salesforce commerce cloud', 'prestashop',
                       'opencart', 'oscommerce', 'drupal commerce', 'sap commerce', 'oracle atg', 'hybris'],

        # Other Categories
        'Other': ['go', 'scala', 'perl', 'rust', 'elixir', 'erlang', 'haskell', 'r', 'matlab', 'lua', 'vhdl', 'verilog',
                  'assembly', 'cobol', 'fortran', 'pascal', 'ada', 'awk', 'bash', 'shell scripting', 'powershell',
                  'tcl', 'f#', 'racket', 'lisp', 'prolog', 'low code', 'no code', 'chatgpt', 'ai tools', 'mlops']
    }

    # Initialize counters for category and subcategory frequencies
    category_counter = Counter()
    subcategory_counter = {category: Counter() for category in categories}

    # Process each job ad
    for ad in job_ads:
        content = ad['content'].lower()  # Convert content to lowercase

        # Count occurrences of each keyword in its category
        for category, keywords in categories.items():
            for keyword in keywords:
                keyword_pattern = re.escape(keyword)
                count = len(re.findall(r'\b{}\b'.format(keyword_pattern), content))
                category_counter[category] += count
                subcategory_counter[category][keyword] += count

    # Main category chart
    category_labels, category_frequencies = zip(*sorted(category_counter.items(), key=lambda x: x[1], reverse=True))

    fig = go.Figure()

    # Add category bar chart
    fig.add_trace(go.Bar(
        x=category_labels,
        y=category_frequencies,
        name='Categories',
        visible=True,
    ))

    # Add subcategory charts (initially hidden)
    for category in categories:
        subcategory_labels, subcategory_frequencies = zip(
            *sorted(subcategory_counter[category].items(), key=lambda x: x[1], reverse=True))
        fig.add_trace(go.Bar(
            x=subcategory_labels,
            y=subcategory_frequencies,
            name=f'{category} Details',
            visible=False,
        ))

    # Update layout with buttons
    fig.update_layout(
        title='Job Ad Frequencies by Category and Details',
        xaxis_title='Keywords',
        yaxis_title='Frequency',
        updatemenus=[
            {
                'buttons': [
                               {'label': 'All Categories', 'method': 'update',
                                'args': [{'visible': [True] + [False] * len(categories)},
                                         {'title': 'Job Ad Frequencies by Category'}]},
                           ] + [
                               {'label': category, 'method': 'update', 'args': [
                                   {'visible': [False] * (index + 1) + [True] + [False] * (
                                           len(categories) - index - 1)},
                                   {'title': f'{category} Details'}]} for index, category in enumerate(categories)
                           ],
                'direction': 'down',
            }
        ]
    )

    # Show the plot
    fig.show()


if __name__ == '__main__':
    analysis()
