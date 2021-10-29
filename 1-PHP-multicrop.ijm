//sdir = '/home/fm/Desktop/TFM Processing Trial/200902-TFM40X0.9-30µgmlOKT3/UnactivatedTcells/200PaPAG/aligned/'

// select output dir
sdir = getDirectory("Where to put the cropped stacks ?");

n = roiManager("count");
for (i=0; i<n; i++) {
     segment = "segment_"+i + File.separator;
     ddir = sdir+segment;
     File.makeDirectory(ddir);
     roiManager("select", i);
     run("Duplicate...", "title = segment duplicate range=1-["+n+"]");
     run("Image Sequence... ", "format=TIFF name=["+segment+"] start=0 digits=5 use save=["+ddir+"]");
close();
  } 
showMessage("Done !");
