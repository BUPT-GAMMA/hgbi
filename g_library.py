from openhgnn.dataset import build_dataset
from openhgnn.dataset import AcademicDataset
from openhgnn.dataset import Mg2vecDataSet
import dgl
from dgl.data import DGLDataset
from dgl import transforms as T
from openhgnn.dataset import AsLinkPredictionDataset, AsNodeClassificationDataset

def construct_dataset(name,task):
    if task == 'node_classification':
        if name in [
                    'acm4NSHE', 'acm4GTN', 'academic4HetGNN', 'acm_han_raw',
                    'acm4HeCo', 'dblp4MAGNN', 'imdb4MAGNN', 'imdb4GTN',
                    'acm4NARS', 'yelp4HeGAN',
                    'HGBn-ACM', 'HGBn-DBLP', 'HGBn-Freebase', 'HGBn-IMDB',
                    'alircd_session1',
                    'ohgbn-Freebase', 'ohgbn-yelp2', 'ohgbn-acm', 'ohgbn-imdb',
                    'dblp4GTN',
                    'HNE-PubMed', #修复：应该在节点里，而不是链路预测
                    'ogbn-mag',#下载比较慢
                    'aifb', 'mutag', 'bgs', 'am',
                    ]:
            return build_dataset(dataset=name, task=task, logger=None)
        
        elif name  == "academic4HetGNN":
            return AcademicDataset("academic4HetGNN")
        
        #修复：dblp4Mg2vec_4、dblp4Mg2vec_5大写需要改成 dblp4mg2vec_4 dblp4mg2vec_5
        #没找到mg2vec这个算法，这个是链路预测的吧，没有node label
        elif name in ['dblp4mg2vec_4', 'dblp4mg2vec_5']:
            ds = Mg2vecDataSet(name=name)
            ds.g = ds[0]
            return ds


    elif task == 'link_prediction':
        #amazon4SLICE 使用了节点分类的代码，先去掉
        if name in ['MTWM', 'HGBl-ACM',
                    'HGBl-DBLP', 'HGBl-IMDB',
                    'wn18', 'FB15k', 'FB15k-237',
                    'HGBl-amazon', 'HGBl-LastFM', 'HGBl-PubMed',
                    'ohgbl-MTWM', 'ohgbl-yelp1', 'ohgbl-yelp2', 'ohgbl-Freebase']:   
            return build_dataset(dataset=name, task=task, logger=None)
        elif name in ['DoubanMovie']: #修复，需要单独拿出来，原来hin_nodeclassification注册类里面没有
            ds = AcademicDataset('DoubanMovie')
            ds.g = ds[0]
            return ds
        

    elif task == 'recommendation':
        if name in ['LastFM4KGCN','yelp4rec']:
            return build_dataset(dataset=name, task=task, logger=None)

class MyDataset(DGLDataset):
    def __init__(self,name,path,reverse=False):
        self.path = path
        self.reverse = reverse
        super().__init__(name=name)
        

    def process(self):
        gs, _ = dgl.load_graphs(self.path)
        gs[0]
        if(self.reverse):
            self._g = T.AddReverse()(gs[0])
        else:
            self._g = gs[0]

    def __getitem__(self, idx):
        return self._g

    def __len__(self):
        return 1

