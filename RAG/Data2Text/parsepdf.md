从PDF文档中提取信息，是很多类似RAG这样的应用第一步要处理的事情，在这个环节，我们需要做好三件事：

提取出来的文本要保持信息完整性，也就是准确性；
提出的结果需要有附加信息，也就是要保存元数据；
提取过程要完成自动化，也就是流程化。
然而，在我们开始之前，我们需要指定目前不同类型的pdf，更具体地说，是出现最频繁的三种:

机器生成的pdf文件：这些pdf文件是在计算机上使用W3C技术(如HTML、CSS和Javascript)或其他软件(如Adobe Acrobat、Word或Typora等MarkDown工具)创建的。这种类型的文件可以包含各种组件，例如图像、文本和链接，这些组件都是可以被选中、搜索和易于编辑的。
传统扫描文档：这些PDF文件是通过扫描仪、手机是的扫描王这样的APP从实物上扫描创建的。这些文件只不过是存储在PDF文件中的图像集合。也就是说，出现在这些图像中的元素，如文本或链接是不能被选择或搜索的。本质上，PDF只是这些图像的容器而已。
带OCR的扫描文档：这种类似有点特殊，在扫描文档后，使用光学字符识别(OCR)软件识别文件中每个图像中的文本，将其转换为可搜索和可编辑的文本。然后软件会在图像上添加一个带有实际文本的图层，这样你就可以在浏览文件时选择它作为一个单独的组件。但是有时候我们不能完全信任OCR，因为它还是存在一定几率的识别错误的。

![parsepdf.png](images%2Fparsepdf.png)

参考链接：
https://www.luxiangdong.com/2023/10/05/extract


引用
https://www.techopedia.com/12-practical-large-language-model-llm-applications
https://www.pdfa.org/wp-content/uploads/2018/06/1330_Johnson.pdf
https://pdfpro.com/blog/guides/pdf-ocr-guide/#:~:text=OCR technology reads text from, a searchable and editable PDF.
https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html#id1
https://github.com/pdfminer/pdfminer.six
Google Tesseract OCR：https://github.com/tesseract-ocr/tesseract