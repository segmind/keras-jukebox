import setuptools

__version__="0.0.3"

with open("README.md","r") as f:
	long_description = f.read()

setuptools.setup(
	name="Keras_JukeBox",
	version=__version__,
	author="T Pratik",
	author_email="pk00095@gmail.com",
	description="A UI based callback for tf-keras",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/pk00095/keras_jukebox/archive/0.0.3.tar.gz",
	packages=setuptools.find_packages(),
	install_requires=['PyQt5','paho-mqtt'],
	entry_points={
		"console_scripts": [
			'start_jukebox=keras_jukebox.jukebox_ui:main']
	},
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux"],
	python_requires='>=3.6')