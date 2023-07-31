import React, { useState } from 'react';
import { Modal, Button, Switch } from 'antd';

import filterIcon from '@iso/assets/images/overview/filter.svg';

function VisibleColumn({ initialConfig, onConfigUpdate }) {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [config, setConfig] = useState({
    ...initialConfig 
  });

  const handleConfigChange = (key, value) => {
    setConfig(prevConfig => ({ ...prevConfig, [key]: value }));
  };

  const handleOk = () => {
    setIsModalVisible(false);
    console.log('Updated config:', config);
    if (onConfigUpdate) {
      onConfigUpdate(config);
    }
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const handleOpenModal = () => {
    setIsModalVisible(true);
  };

  return (
    <div>
      <Button type="secondary" onClick={handleOpenModal} className='button-filter'><img  src={filterIcon} /></Button>
      <Modal
        title="VISIBLE COLUMNS"
        okText="Confirm"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        wrapClassName="filter-modal"
        closable={false}
      >
        <div className='filter-list'>
          <div className='filter-item'>
            <span>Nodes</span>
            <Switch checked={config.nodes} onChange={(checked) => handleConfigChange('nodes', checked)} />
          </div>
          <div className='filter-item'>
            <span>Age</span>
            <Switch checked={config.age} onChange={(checked) => handleConfigChange('age', checked)} />
          </div>
          <div className='filter-item'>
            <span>Action</span>
            <Switch checked={config.action} onChange={(checked) => handleConfigChange('action', checked)} />
          </div>
          <div className='filter-item'>
            <span>ISP</span>
            <Switch checked={config.isp} onChange={(checked) => handleConfigChange('isp', checked)} />
          </div>
          <div className='filter-item'>
            <span>Bond</span>
            <Switch checked={config.bond} onChange={(checked) => handleConfigChange('bond', checked)} />
          </div>
          <div className='filter-item'>
            <span>Providers</span>
            <Switch checked={config.providers} onChange={(checked) => handleConfigChange('providers', checked)} />
          </div>
          <div className='filter-item'>
            <span>Rewards</span>
            <Switch checked={config.rewards} onChange={(checked) => handleConfigChange('rewards', checked)} />
          </div>
          <div className='filter-item'>
            <span>APY</span>
            <Switch checked={config.apy} onChange={(checked) => handleConfigChange('apy', checked)} />
          </div>
          <div className='filter-item'>
            <span>Slashes</span>
            <Switch checked={config.slashes} onChange={(checked) => handleConfigChange('slashes', checked)} />
          </div>
          <div className='filter-item'>
            <span>Score</span>
            <Switch checked={config.score} onChange={(checked) => handleConfigChange('score', checked)} />
          </div>
          <div className='filter-item'>
            <span>Version</span>
            <Switch checked={config.version} onChange={(checked) => handleConfigChange('version', checked)} />
          </div>
          <div className='filter-item'>
            <span>RPC</span>
            <Switch checked={config.rpc} onChange={(checked) => handleConfigChange('rpc', checked)} />
          </div>
          <div className='filter-item'>
            <span>BFR</span>
            <Switch checked={config.bfr} onChange={(checked) => handleConfigChange('bfr', checked)} />
          </div>
        </div>
      </Modal>

    </div>
  );
}

export default VisibleColumn;