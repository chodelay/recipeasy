#!/usr/bin/python
import os, subprocess
import re

COLWIDTH = 6
COLWIDTH_STEPS = 4
DELIMITER = ';'
RECIPE_DIR = 'recipes/'

HEAT_REGEX = "((medium(( |-)(low|high)?)|low|high) heat|([0-9]{2,3}-)?([0-9]{2,3})C)"
TIME_REGEX = "([0-9.]{1,5}(( to |-)[0-9.]{1,5})? min((ute)?)(s?))|([0-9]{1,5} hour(s?))"

def iconHTML(glyph, link):
  html = '<button type="button" class="btn btn-default" aria-label="' + glyph + '" onclick="window.location.href = \'/' + link + '\';">'
  html += '<span class="glyphicon glyphicon-' + glyph +'" aria-hidden="true"></span></button>'
  return html

def getTimeFromString(string):
  retval = 0
  if string == '':
    retval = int(0)
  elif string =="1 hour":
    retval = 60
  elif len(string.split("hours")) > 1:
    retval = int(string.split("hours")[0].rstrip(' '))*60
  elif len(string.split("min")) > 1:
    retval = int(string.split("min")[0].rstrip(' '))
  elif len(string.split("hrs")) > 1:
    retval = int(string.split("hrs")[0].rstrip(' '))
  return int(retval)

def getRecipeTime(recipeName):
  totalTime = 0;
  dirlist = os.listdir(RECIPE_DIR + recipeName + '/steps')
  dirlist.sort()
  for step in dirlist:
    with open(RECIPE_DIR + recipeName + '/steps/' + step, "r") as f:
      timeline = f.readline()
      timers = timeline.split(';')
      if len(timers) == 2:
        totalTime += getTimeFromString(timers[1].rstrip('\n.'))
      else:
        totalTime += getTimeFromString(timers[0].rstrip('\n.'))
  # print totalTime
  return totalTime

# Import dependencies
def scriptHTML(folderPrefix, useCustom):
  html = '<head>'
  html = '<link rel="stylesheet" type="text/css" href="' + folderPrefix + 'css/bootstrap.css">'
  html += '<link rel="stylesheet" type="text/css" href="' + folderPrefix + 'css/styles.css">'
  html += '<link href="https://fonts.googleapis.com/css?family=Mukta+Malar|Oxygen" rel="stylesheet">'
  #html += '<script type="javascript" src="/js/jquery-3.2.1.min.js"/></script>'
  html += '<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>'
  html += '<script type="text/javascript" src="' + folderPrefix + 'js/bootstrap.js"></script>'
  html += '</head><body>'
  html += '<script type="text/javascript" src="' + folderPrefix + 'js/custom.js"/></script>' if useCustom else ''
  return html

# Title Bar
def titleHTML(recipeName, hasBack):
  recipename = recipeName.replace('-', ' ').title()
  html = '<div class="container recipe-title-container">'
  html += '<div class="row recipe-title">'
  html += '<div class="col-sm-1 text-center">'
  button = iconHTML('chevron-left', '')
  html = html + button if hasBack else html
  html += '</div><div class="col-sm-10 text-center"><h1>' + recipename + '</h1></div>'
  html += '</h1><div class="col-sm-1 text-center">'
  button = iconHTML('print', RECIPE_DIR + recipeName + '/print.html')
  html += button if hasBack else ''
  html += '</div></div></div>'
  return html

# Get all ingredients
def ingredientsHTML(recipeName, hasContract):
  directory = RECIPE_DIR + recipeName + '/ingredients'
  html = '<div class="container">'
  html += '<div class="row"><div class="col-sm-11">'
  html += '<h2>Ingredients</h2></div>'

  html += '<div class="col-sm-1 text-center">'
  button = '<button class="toggle" onclick="hideElement(\'ingredient-row\');" label="o"></button>'
  html += button if hasContract else ''
  html += '</div></div><div class="row" id="ingredient-row">'

  dirlist = os.listdir(directory)
  dirlist.sort()

  for file in dirlist:
    filetitle = ''.join(i for i in file.replace('-',' ') if not i.isdigit()).title()
    html += '<div class="col-md-' + str(COLWIDTH) + '"><table><tr><h3>' + filetitle + '</h3></tr>'

    with open(directory+'/'+file, "r") as f:
      for line in f:
        row = line.split(DELIMITER)
        html += '<tr><td class="amount-text">' + row[0] + '</td><td class="item-text">'
        if len(row) > 1:
          html += row[1].title() + '</td><td class="note-text">'
        else:
          html += '</td></tr>'
        if len(row) > 2:
          html += row[2] + '</td></tr>'
        else:
          html += '</td></tr>'

    html += '</table></div>'

  html += '</div></div>'
  return html

# Get all utensils
def utensilsHTML(recipeName, hasContract):
  directory = RECIPE_DIR + recipeName + '/utensils'
  html = '<div class="container">'
  html += '<div class="row"><div class="col-sm-11">'
  html += '<h2>Utensils</h2></div>'

  # Toggle Section div
  html += '<div class="col-sm-1 text-center">'
  button = '<button class="toggle" onclick="hideElement(\'utensils-row\');" text="o"></button>'
  html += button if hasContract else ''
  html += '</div></div><div class="row" id="utensils-row">'

  dirlist = os.listdir(directory)
  dirlist.sort()

  for file in dirlist:
    filetitle = ''.join(i for i in file.replace('-',' ') if i.isalpha()).title()
    if filetitle != '':
      html += '<div class="col-md-' + str(COLWIDTH_STEPS) + '"><table><tr><th><h3>' + filetitle + '</h3></th></tr>'
    else:
      html += '<div class="col-md-' + str(COLWIDTH_STEPS) + '"><table>'

    with open(directory+'/'+file, "r") as f:
      for line in f:
        row = line.split(DELIMITER)
        html += '<tr>'
        html += '<td class="amount-text">' + row[0] + '</td><td class="item-text">' if row else ''
        if len(row) > 1:
          html += row[1].title() + '</td></tr>'
        else:
          html += '</td></tr>'

    html += '</table></div>'

  html += '</div></div>'
  return html

# Get steps
def stepsHTML(recipeName, hasContract):
  directory = RECIPE_DIR + recipeName + '/steps'
  html = '<div class="container">'
  html += '<div class="row"><div class="col-sm-11">'
  html += '<h2>Steps</h2></div>'

  # Toggle Section div
  html += '<div class="col-sm-1 text-center">'
  button = '<button class="toggle" onclick="hideElement(\'steps-row\');"></button>'
  html += button if hasContract else ''
  html += '</div>'

  html += '</div><div class="row" id="steps-row">'

  dirlist = os.listdir(directory)
  dirlist.sort()

  i = 1;
  for file in dirlist:
    filetitle = ''.join(i for i in file.replace('-',' ') if not i.isdigit()).title()
    html += '<div class="col-md-' + str(COLWIDTH_STEPS) + '"><h3 class="step-header">' + str(i) + '. ' + filetitle + '</h3>'
    i += 1;
    first = True
    # Open File
    with open(directory+'/'+file, "r") as f:
      timeline = f.readline()
      timers = timeline.split(';')
      if len(timers) == 2:
        html += '<div class="row">'
        html += '<div class="timer_active col-xs-6">' + timers[0] + '</div><div class="timer_inactive col-xs-6">' + timers[1] + '</div>'
        html += '</div>'
      else:
        html += '<div class="row">'
        html += '<div class="timer_active col-xs-12">' + timers[0] + '</div>'
        html += '</div>'

      html += '<ul>'
      for line in f:
        # Add time spans
        # print line
        #print TIME_REGEX
        line = re.sub(TIME_REGEX, '<span class="time-text">\\1</span>', line)

        line = re.sub(HEAT_REGEX, '<span class="heat-text">\\1</span>', line)

        if line.strip():
          html += '<li>' + line + '</li>'

    html += '</ul></div>'

  html += '</div></div>'

  return html

def pictureHTML(recipeName):
  html = '<div class="container"><div class="row">'
  html += '<div class="col-xs-11"></div>'
  html += '<div class="col-xs-1">'
  html += '<button class="toggle" onclick="hideElement(\'image-col\');"></button>'
  html += '</div>'
  html += '</div><div class="row">'
  html += '<div class="col-xs-12 text-center" id="image-col">'
  html += '<img src="../../recipes/' + recipeName + '/img.png" alt="' + recipeName + '" height="160", width="300"></img>'
  html += '</div></div></div>'
  return html

def linkHTML():
  html = '<div class="container"><div class="row">'
  dirlist = os.listdir('recipes')
  dirlist.sort()

  for folder in dirlist:
    linktitle = folder.replace('-',' ').title()
    html += '<div class="col-md-4 recipe-link-col">'
    html += '<div class="container"><div class="row"><div class="col-md-12">'
    html += '<a class="recipe-link" href="recipes/' + folder + '/recipe.html">' + linktitle + '</a>'
    html += '</div><div class="col-md-12 time-text">'
    html += str(getRecipeTime(folder)) + ' min'
    html += '</div><div class="col-md-12">'
    html += '<img src="recipes/' + folder + '/img.png" alt="' + linktitle + '" height="100", width="100"></img>'
    html += '</div></div></div></div>'
    # print 'Building ', folder
    buildRecipe(folder)
  html += '</div></div>'
  return html

def buildRecipe(recipeName):
  html = scriptHTML('../../', True)
  html += titleHTML(recipeName, True)
  html += pictureHTML(recipeName)
  html += ingredientsHTML(recipeName, True)
  html += utensilsHTML(recipeName, True)
  html += stepsHTML(recipeName, True)
  html += '</body>'
  file = open(RECIPE_DIR + recipeName + '/recipe.html', 'w')
  file.write(html)
  file.close()

  # Build Printable Version
  html = scriptHTML('../../', False)
  html = titleHTML(recipeName, False)
  html += ingredientsHTML(recipeName, False)
  html += utensilsHTML(recipeName, False)
  html += stepsHTML(recipeName, False)
  html += '</body>'
  file = open(RECIPE_DIR + recipeName + '/print.html', 'w')
  file.write(html)
  file.close()

def buildIndex():
  html = scriptHTML('', False)
  html += titleHTML('Recipeasy', False)
  html += linkHTML()
  html += '</body>'
  file = open('index.php', 'w')
  file.write(html)
  file.close()

buildIndex()
