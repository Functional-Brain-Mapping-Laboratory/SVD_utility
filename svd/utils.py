import os

import pandas as pd
import numpy as np
import numpy as np
import pycartool
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import explained_variance_score


def compute_explained_variance_score(X, svd):
    y_true = X
    y_pred = svd.inverse_transform(svd.transform(y_true))
    score = explained_variance_score(y_true, y_pred)
    return (score)


def fit_svds(ris_files, rois):
    # init
    init_ris = pycartool.source_estimate.read_ris(ris_files[0])
    shape = init_ris.sources_tc.shape
    sfreq = init_ris.sfreq
    # compute
    svds = []
    vars = []
    for i, roi in enumerate(rois.groups_of_indexes):
        data = []
        for file in ris_files:
            ris = pycartool.source_estimate.read_ris(file)
            if ris.sources_tc.shape != shape:
                raise ValueError('All files must share the same number of sources.')
            data.append(ris.sources_tc[roi])
        data = np.concatenate(data, axis=-1)
        # reshape
        data = data.reshape(-1, data.shape[-1])
        if data.shape[0] == 1:
            tc = np.array([data[0]]).T
            var = 1
        else:
            tmp_data = data.T
            svd = TruncatedSVD(n_components=1)
            svd.fit(tmp_data)
            var = compute_explained_variance_score(tmp_data, svd)
        svds.append(svd)
        vars.append(var)
    return(svds, vars)


def transform_files(file, svds, rois, scaling, output_directory):
    fname_out = os.path.basename(file)
    fname_out = os.path.splitext(fname_out)[0]
    fname_out = fname_out + '_rois.ris'
    fname_out = os.path.join(output_directory, fname_out)

    ris = pycartool.source_estimate.read_ris(file)
    sfreq = ris.sfreq
    rois_tc = list()
    rois_var = list()
    for i, roi in enumerate(rois.groups_of_indexes):
        data = ris.sources_tc[roi]
        data = data.reshape(-1, data.shape[-1])
        svd = svds[i]
        if data.shape[0] == 1:
            tc = np.array([data[0]]).T
            var = 1
        else:
            tmp_data = data.T
            tc = svd.transform(tmp_data)
            var = compute_explained_variance_score(tmp_data, svd)
            if scaling == 'Eigenvalue':
                tc = tc * svd.singular_values_[0]
            elif scaling == 'None':
                pass
            else:
                raise ValueError('unknown scaling method')
        rois_tc.append(tc)
        rois_var.append(var)
    rois_ris = pycartool.source_estimate.SourceEstimate(np.array(rois_tc).swapaxes(1,2), sfreq)
    rois_ris.save(fname_out)
    return(fname_out, rois_var)


def transform_svds(ris_files, rois, scaling, output_directory):
    stat_file = os.path.join(output_directory, 'Explained_variance_regression_scores.csv')
    svds, vars = fit_svds(ris_files, rois)
    all_scores = list()
    all_fname_out = list()
    for file in ris_files:
        fname_out, rois_var = transform_files(file,
                                              svds,
                                              rois,
                                              scaling,
                                              output_directory)
        all_scores.append(rois_var)
        all_fname_out.append(fname_out)

    rois_var = np.array(all_scores)
    all_fname_out = [os.path.basename(fname) for fname in all_fname_out]
    df = pd.DataFrame(rois_var.T, index=rois.names, columns=all_fname_out)
    df['Fit'] = vars
    df.to_csv(stat_file, sep=';')
