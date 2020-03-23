from distutils.core import setup
setup(
  name = 'cisco-sdwan-policy',         # How you named your package folder (MyLib)
  packages = ['cisco_sdwan_policy','cisco_sdwan_policy.Helper','cisco_sdwan_policy.List','cisco_sdwan_policy.LocalPolicy','cisco_sdwan_policy.Topology','cisco_sdwan_policy.TrafficPolicy'],   # Chose the same as "name"
  version = '0.41',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A module for easy add/modify policies to Cisco SD-WAN(Viptela)',   # Give a short description about your library
  author = 'Jiaming Li',                   # Type in your name
  author_email = 'jiaminli@cisco.com',      # Type in your E-Mail
  url = 'https://github.com/ljm625/cisco_sdwan_policy_python',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ljm625/cisco_sdwan_policy_python/archive/v0.35.tar.gz',    # I explain this later on
  keywords = ['SDWAN', 'CiSCO', 'REST'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  scripts=['bin/sdwan-policy-tool','bin/sdwan-template-tool','bin/sdwan-apps-generator'],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
