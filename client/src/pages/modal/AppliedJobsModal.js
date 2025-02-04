import React from 'react';
import JobCard from '../../component/JobCard';
import './AppliedJobsModal.css';

const AppliedJobsModal = ({ isOpen, onClose, appliedJobs, favoriteCompanies, bookmarkedJobs, onToggleFavorite, onToggleBookmark, onToggleApplied }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>지원 완료한 공고</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          {appliedJobs.length > 0 ? (
            appliedJobs.map((job) => (
              <JobCard
                key={job.post_id}
                job={job}
                favoriteCompanies={favoriteCompanies}
                bookmarkedJobs={bookmarkedJobs}
                appliedJobs={appliedJobs.map(j => j.post_id)}
                onToggleFavorite={onToggleFavorite}
                onToggleBookmark={onToggleBookmark}
                onToggleApplied={onToggleApplied}
              />
            ))
          ) : (
            <p>지원한 공고가 없습니다.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AppliedJobsModal;