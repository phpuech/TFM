//sdir = '/home/fm/Desktop/TFM Processing Trial/200902-TFM40X0.9-30µgmlOKT3/UnactivatedTcells/200PaPAG/aligned/'

function TFMcalc(start, current, inputdir, outputdir, index, youngmodulus, pixelsize) { 
	run("Close All");
	open(inputdir+start);
	open(inputdir+current);
	print(inputdir+start);
	print(inputdir+current);
	run("Images to Stack","title=[]");
	//makeRectangle(3, 1, 78, 76);
	//run("Align slices in stack...", "method=5 windowsizex=78 windowsizey=76 x0=3 y0=1 swindow=0 subpixel=true itpmethod=0 ref.slice=1 show=true");
	sortie="PIV_"+index+".txt";
	output=outputdir+sortie;
	print(output);
	file=File.open(output);
	print(youngmodulus);
	run("iterative PIV(Advanced)...", "  piv1=64 sw1=128 vs1=32 piv2=32 sw2=64 vs2=16 piv3=16 sw3=32 vs3=8 correlation=0.60 debug_x=-1 debug_y=-1 path=/save/ what=[Accept this PIV and output] noise=0.20 threshold=5 c1=3 c2=1 save=[output]");
	File.close(file);
	
	run("FTTC ", "pixel=pixelsize poisson=0.5 young's=youngmodulus regularization=0.0000000009 plot plot_0=widthimage plot_1=widthimage select=[output]");

}



// select output dir
sdir = getDirectory("Where to put the cropped stacks ?");

//n = roiManager("count");
//for (i=0; i<n; i++) {
//     segment = "segment_"+i + File.separator;
//     ddir = sdir+segment;
//     File.makeDirectory(ddir);
//     roiManager("select", i);
//     run("Duplicate...", "title = segment duplicate range=1-["+n+"]");
//     run("Image Sequence... ", "format=TIFF name=["+segment+"] start=0 digits=5 use save=["+ddir+"]");
//close();
//  } 
//showMessage("Done !");

mainDir = sdir; 
mainList = getFileList(mainDir); 

for (k = 0; k < mainList.length; k++) {
     if(startsWith(mainList[k], "segment")){
			print(mainList[k]);
	
	        inputdir = mainDir + mainList[k];
	        print(inputdir);
	        
	        outputdir = inputdir+"save/";
			
			var reference=0;
			var widthimage=128;
			var youngmodulus=400;
			var pixelsize=0.1577;
			var widthimage=128;

			print(inputdir);
			setBatchMode(true); 
			list = getFileList(inputdir);
			//for (i = 0; i < list.length; i++){
			//        print(list[i]);
			//}
			
			
			File.makeDirectory(outputdir);
			
			print("\\Clear");
			print("Begin");
			print("-----------------------------------------------------");
			for (i = reference+1; i < list.length; i++){
					print(list[reference]);
			        TFMcalc(list[reference], list[i], inputdir, outputdir, i, youngmodulus, pixelsize);
			        print("-----------------------------------------------------");
			}
			run("Collect Garbage");
			print("End");
		
     } else {print("poop");}
}