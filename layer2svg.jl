#! /usr/local/bin/julia
using EzXML
function splitFile(procString::String)
  rootPath=splitdir(procString)[1]
  origDoc=readxml(procString)
  origRoot=root(origDoc)
  origNamespace=namespaces(origRoot)
  origAttribute=attributes(origRoot)
  origElement=elements(origRoot)

  # Sort out layers
  isLayer=Vector{Bool}(undef,length(origElement))
  isBackground=Vector{Bool}(undef,length(origElement))
  layerNames=Vector{String}(undef,length(origElement))

  fill!(isLayer,false)
  fill!(isBackground,false)
  fill!(layerNames,"")

  for ii in 1:length(origElement)  # Find the various layers
    tempAtt=attributes(origElement[ii])
    for jj in 1:length(tempAtt)
      # println(tempAtt[jj].name," => ",tempAtt[jj].content)
      if tempAtt[jj].name=="groupmode" && tempAtt[jj].content == "layer"
        isLayer[ii]=true;
      end
      if tempAtt[jj].name=="label"
        layerNames[ii]=tempAtt[jj].content;
      end
      if tempAtt[jj].name=="label" && lowercase(tempAtt[jj].content) == "background"
        isBackground[ii]=true;
      end
    end
  end

  isLayer=isLayer.&.~isBackground  #Work out which ones to keep
  layerIndex=(1:length(isLayer))[isLayer]
  permIndex=(1:length(isLayer))[.~isLayer.|isBackground]

  for layerNo in layerIndex   #Create new files
    # Reassemble file
    currDoc=XMLDocument()
    currRoot=setroot!(currDoc,ElementNode(origRoot.name))
    unlink!.(origAttribute)
    link!.(Ref(currRoot),origAttribute)
    # Preseve namespace hack
    for tt in 1:length(origNamespace)
      if length(origNamespace[tt][1])>1
        link!(currRoot,AttributeNode(string("xmlns:",origNamespace[tt][1]),origNamespace[tt][2]))
      else
        link!(currRoot,AttributeNode(string("xmlns",origNamespace[tt][1]),origNamespace[tt][2]))
      end
    end
    currIndex=cat(permIndex,layerNo,dims=1)
    unlink!.(origElement)
    for ll in currIndex
      link!(currRoot,origElement[ll])
    end
    println(layerNames[layerNo])
    write(rootPath*"/"*layerNames[layerNo]*".svg",currDoc)
  end
end

absP=abspath.(ARGS)
splitFile.(absP)
